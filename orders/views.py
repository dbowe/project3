from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

import json

from .models import Pizza, Sub, Topping, Platter, Pasta, Salad, Extra, PizzaPricing, Order

myShoppingCart = {}
# Ask user to log in or create an account
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": "Please create an account for online ordering"})

    context = {
        "user": request.user
    }
    return render(request, "orders/login.html", context, {"message": "Welcome back"})


# display the menu.  need to deal with username
def menu_view(request):
    menu = get_menu()
    return render(request, "orders/menu.html", menu)
    
def get_menu():
    allPizzas = Pizza.objects.all()
    pizzaRegSmPrices = PizzaPricing.objects.filter(pizzaType="R", pizzaSize="S").order_by("pizza_price")
    pizzaRegLgPrices = PizzaPricing.objects.filter(pizzaType="R", pizzaSize="L").order_by("pizza_price")
    pizzaRegPrices = zip(pizzaRegSmPrices, pizzaRegLgPrices)
    pizzaSicilianSmPrices = PizzaPricing.objects.filter(pizzaType="S", pizzaSize="S").order_by("pizza_price")
    pizzaSicilianLgPrices = PizzaPricing.objects.filter(pizzaType="S", pizzaSize="L").order_by("pizza_price")
    pizzaSicilianPrices = zip(pizzaSicilianSmPrices, pizzaSicilianLgPrices)

    toppings = Topping.objects.all()
    subs = Sub.objects.all()
    salads = Salad.objects.all()
    platters = Platter.objects.all()
    pastas = Pasta.objects.all()
    cheese = Extra.objects.filter(type="Extra Cheese")[0]
    extras = Extra.objects.exclude(type= "Extra Cheese")

    context = {
        "allPizzas": allPizzas,
        "pizzaRegPrices": pizzaRegPrices,
        "pizzaSicilianPrices": pizzaSicilianPrices,
        "toppings": toppings,
        "subs": subs,
        "cheese": cheese,
        "extras": extras,
        "salads": salads,
        "platters": platters,
        "pastas": pastas,
        }
    return (context)

# Log user in and display menu
def login_view(request):
    username = request.POST["username"]
    try: 
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    # No user with that name; try to register
    if user is None:
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password_confirmation"]
        # Check for matching passwords
        if password != password2:
            return render(request, "orders/login.html", {"message": "Passwords do not match"})

        # Create new user and log him/her in
        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.username = username
        user.save()
    else: 
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})

    # Finally, log in the user and display the menu

    login(request, user)

    context = get_menu()
    context["username"] = username
    return render(request, "orders/menu.html", context)

def emptyMyCart(user):
    if user in myShoppingCart:
        myShoppingCart[user]["myItems"] = []
        myShoppingCart[user]["Total"] = 0
    else:
        print (f"No such cart: ", user)
    return True
        
# Empty Shopping cart
def emptyCart(request):
    emptyMyCart(request.user.id)
    menu = get_menu()
    return render(request, "orders/orderOnline.html", menu)

# View Order History
def viewOrders(request):
    user_id = request.user.id

    orders = Order.objects.filter(customer=user_id)
        
    context = {
        "myOrders": orders,
        }
    return render(request, "orders/viewOrders.html", context)

# View Shopping cart
def shoppingCart(request):

    user_id = request.user.id
    if user_id not in myShoppingCart:
        myShoppingCart[user_id] = {"Total": 0, "myItems": []}
        
    add_toppings=[]
    if 'pizza' in request.POST and request.POST["pizza"]:
        details = request.POST["pizza"]
        size = details[0]
        type = details[1]
        new_item = {"size": size, 
                    "itemType": "pizza", 
                    "type": type } 
        if 'topping' in request.POST:
            add_toppings = request.POST.getlist('topping')
            num_toppings = len(add_toppings)
            priceObj = PizzaPricing.objects.get(pizzaType = type, pizzaSize = size, numToppings = num_toppings)
            new_item["toppings"] = add_toppings
        else:
            priceObj = PizzaPricing.objects.get(pizzaType = type, pizzaSize = size, numToppings = 0)

        new_item["price"] = priceObj.pizzaPrice
        if user_id in myShoppingCart:
            myShoppingCart[user_id]["Total"] += priceObj.pizzaPrice
            myShoppingCart[user_id]["myItems"].append(new_item)
        else: 
            myShoppingCart[user_id] = {"myItems": [new_item], 
                                       "Total": priceObj.pizzaPrice}
        myShoppingCart[user_id]["pizza"] = new_item

    if 'sub' in request.POST and request.POST['sub']:
        subs = request.POST.getlist('sub')
        for next_sub in subs:
            size = next_sub[0]
            subType = next_sub[1:]
            subObj = Sub.objects.get(type=subType)
            exPrice = 0
            new_item = {"size": size, 
                        "itemType": "sub", 
                        "type": subType } 
            if size == "S":
                price = subObj.smPrice
            else:
                price = subObj.lgPrice
            if subType == "Steak + Cheese":
                if 'extras' in request.POST:
                    addOns = request.POST.getlist("extras")
                    for addOn in addOns:
                        ex = Extra.objects.get(type=addOn)
                        exPrice += ex.price
                new_item["extras"] = addOns
            price += exPrice
            new_item["price"] = price
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], 
                                           "Total": price}
                                 
    if 'platter' in request.POST and request.POST['platter']:
        platters = request.POST.getlist('platter')
        for next_platter in platters:
            size = next_platter[0]
            platterType = next_platter[1:]
            platterObj = Platter.objects.get(type=platterType)
            new_item = {"size": size, 
                        "itemType": "platter", 
                        "type": platterType } 
            if size == "S":
                price = platterObj.smPrice
            else:
                price = platterObj.lgPrice
            new_item["price"] = price
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], 
                                           "Total": price}
                                 
    if 'salad' in request.POST and request.POST['salad']:
        salads = request.POST.getlist('salad')
        for next_salad in salads:
            saladObj = Salad.objects.get(type=next_salad)
            new_item = {"size": "One size", 
                        "itemType": "salad", 
                        "type": next_salad,
                        "price": saladObj.price
                        } 
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += saladObj.price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], 
                                           "Total": saladObj.price}
                                 
    if 'pasta' in request.POST and request.POST['pasta']:
        pastas = request.POST.getlist('pasta')
        for next_pasta in pastas:
            pastaObj = Pasta.objects.get(type=next_pasta)
            price = pastaObj.price
            new_item = {"size": "", 
                        "itemType": "pasta", 
                        "type": next_pasta,
                        "price":price }
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], 
                                           "Total": price}

    context = {
        "cart": myShoppingCart[user_id]["myItems"],
        "total": myShoppingCart[user_id]["Total"],
        }
    return render(request, "orders/shoppingCart.html", context)

# Place an online order
def orderOnline(request):
    menu = get_menu()
    return render(request, "orders/orderOnline.html", menu)

# Display order for confirmation
def placeOrder_view(request, methods=["POST"]):
    user_id = request.user.id

    if user_id not in myShoppingCart:
        menu = get_menu()
        return render (request, "orders/orderOnline.html", menu)

    orderItems = myShoppingCart[user_id]["myItems"]
    orderTotal = myShoppingCart[user_id]["Total"]
    user = User.objects.get(pk=user_id)
    order = Order.objects.create(total=orderTotal, customer=user, itemList=orderItems)
    order.save()
    emptyMyCart(user_id)

    context = get_menu()
    context["username"] = user.username
    return render(request, "orders/menu.html", context)
#    return render(request, "orders/menu.html", context, {"message": "Order Placed!!"})

# Goodbye
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
