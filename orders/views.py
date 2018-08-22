from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Pizza, Sub, Topping, Platter, Pasta, Salad, Extra, PizzaPricing, Order, Customer

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
    user = User.objects.get(username=username)

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
        # Check if username already in use
        user = User.objects.get(username=username)
        if user is not None:
            return render(request, "orders/login.html", {"message": "Username exists.  Please choose another."})

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

# View Shopping cart
def shoppingCart(request):

#    if request.user not in myShoppingCart:
#        myItems = ["Cart is Empty"]
#        context = {"cart": myItems, "Total": 0}
#        return render(request, "orders/shoppingCart.html", context)
    user_id = request.user.id

    add_toppings=[]
    if 'pizza' in request.POST and request.POST["pizza"]:
        details = request.POST["pizza"]
        size = details[0]
        type = details[1]
        new_item = {"size": size, "itemType": "pizza", "type": type } 
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
            myShoppingCart[user_id] = {"myItems": [new_item], "Total": priceObj.pizzaPrice}
        myShoppingCart[user_id]["pizza"] = new_item

    if 'sub' in request.POST and request.POST['sub']:
        subs = request.POST.getlist('sub')
        for next_sub in subs:
            size = next_sub[0]
            subType = next_sub[1:]
            subObj = Sub.objects.get(type=subType)
            new_item = {"size": size, "itemType": "sub", "type": subType } 
            if size == "S":
                price = subObj.smPrice
            else:
                price = subObj.lgPrice
            new_item["price"] = price
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], "Total": price}
                                 
    if 'platter' in request.POST and request.POST['platter']:
        platters = request.POST.getlist('platter')
        for next_platter in platters:
            size = next_platter[0]
            platterType = next_platter[1:]
            platterObj = Platter.objects.get(type=platterType)
            new_item = {"size": size, "itemType": "platter", "type": platterType } 
            if size == "S":
                price = platterObj.smPrice
            else:
                price = platterObj.lgPrice
            new_item["price"] = price
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], "Total": price}
                                 
    if 'salad' in request.POST and request.POST['salad']:
        salads = request.POST.getlist('salad')
        for next_salad in salads:
            saladObj = Salad.objects.get(type=next_salad)
            new_item = {"size": "", "itemType": "salad", "type": next_salad } 
            new_item["price"] = saladObj.price
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += saladObj.price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], "Total": saladObj.price}
                                 
    if 'pasta' in request.POST and request.POST['pasta']:
        pastas = request.POST.getlist('pasta')
        for next_pasta in pastas:
            pastaObj = Pasta.objects.get(type=next_pasta)
            price = pastaObj.price
            new_item = {"size": "", "itemType": "pasta", "type": next_pasta } 
            new_item["price"] = price
            if user_id in myShoppingCart:
                myShoppingCart[user_id]["Total"] += price
                myShoppingCart[user_id]["myItems"].append(new_item)
            else: 
                myShoppingCart[user_id] = {"myItems": [new_item], "Total": price}

    print (f"shoppingCart: myItems = ", myShoppingCart[user_id]["myItems"])
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

    orderItems = myShoppingCart[user_id]["myItems"]
    orderTotal = myShoppingCart[user_id]["Total"]

    print (f"placeOrder: user = ", user_id, "total = ", myShoppingCart[user_id]["Total"])

    order = Order.objects.create(total=orderTotal)

    # Get this customer's orders
    customer = Customer.objects.get(pk=user_id)
    if customer is None:
        customer = Customer()
        customer.username = request.user["username"]

    #add each item to a new order
    order.itemList = str(orderItems)
    order.save()
    customer.orders.add(order)
    customer.save()
    emptyMyCart(user_id)
    return render(request, "orders/login.html", {"message": "Order Placed!!"})

# Goodbye
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
