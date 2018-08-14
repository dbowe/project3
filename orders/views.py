from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import Pizza, Sub, Toppings, Platter, Pasta, Salad, Extras

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    context = {
        "user": request.user
    }
    return render(request, "orders/login.html", context)


def menu(request):
    regSmPizzas = Pizza.objects.filter(type='R', size='S')[0]
    regLgPizzas = Pizza.objects.filter(type='R', size='L')[0]
    sicilianSmPizzas = Pizza.objects.filter(type='S', size='S')[0]
    sicilianLgPizzas = Pizza.objects.filter(type='S', size='L')[0]
    toppings = Toppings.objects.all()
    subs = Sub.objects.all()
    salads = Salad.objects.all()
    platters = Platter.objects.all()
    pastas = Pasta.objects.all()
    cheese = Extras.objects.filter(type="Extra Cheese")[0]
    extras = Extras.objects.exclude(type= "Extra Cheese")

    context = {
        "regSmPizzas": regSmPizzas,
        "regLgPizzas": regLgPizzas,
        "sicilianSmPizzas": sicilianSmPizzas,
        "sicilianLgPizzas": sicilianLgPizzas,
        "toppings": toppings,
        "subs": subs,
        "cheese": cheese,
        "extras": extras,
        "salads": salads,
        "platters": platters,
        "pastas": pastas
        }
                                                             
    return render(request, "orders/menu.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("menu"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def register_view(request):
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    username = request.POST["username"]
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
    user.save()
    login(request, user)
    return HttpResponseRedirect(reverse("menu"))

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
