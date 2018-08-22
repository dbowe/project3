from django.db import models
from django.contrib.auth.models import User

# Create your models here.
SIZES = (
    ("S", "Small"),
    ("L", "Large"),
    )
TYPES = (
    ("R", "Regular"),
    ("S", "Sicilian"),
    )

class PizzaPricing(models.Model):
    pizzaType = models.CharField(max_length=1, choices=TYPES)
    pizzaSize = models.CharField(max_length=1, choices=SIZES)
    numToppings = models.IntegerField()
    pizzaPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pizzaSize} {self.pizzaType} with {self.numToppings} toppings = ${self.pizzaPrice}"

class Topping(models.Model):
    type = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f"{self.type}"


class ExtraPricing(models.Model):
    num_extra = models.CharField(max_length=20, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.num_extra} adds {self.price}"
    
class Pizza(models.Model):
    type = models.CharField(max_length=1, choices=TYPES)
    size = models.CharField(max_length=1, choices=SIZES)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="pizza_topping")
    pricing = models.ForeignKey(PizzaPricing, on_delete=models.CASCADE, related_name="pizza_price")

    def __str__(self):
        return f"[{self.size}][{self.type}]"

class Extra(models.Model):
    type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} ${self.price}"

class Sub (models.Model):
    type = models.CharField(max_length=64, blank=False)
    extras = models.ManyToManyField(Extra, blank=True, related_name="sub_extras")
    smPrice = models.DecimalField(max_digits=5, decimal_places=2)
    lgPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} Small: ${self.smPrice} Large: ${self.lgPrice}"

class Salad(models.Model):
    type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type}"

class Pasta(models.Model):
    type = models.CharField(max_length=30, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type}"

class Platter(models.Model):
    type = models.CharField(max_length=30, blank=False)
    smPrice = models.DecimalField(max_digits=5, decimal_places=2)
    lgPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} ${self.smPrice} ${self.lgPrice}"

class Order(models.Model):
    itemList = models.CharField(max_length = 2000)
    total = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.date} {self.total}"

class Customer(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_name")
    orders = models.ManyToManyField(Order, blank=True)

    def __str__(self):
        return f"{self.username}"
