from django.db import models

# Create your models here.
SIZES = (
    ("S", "Small"),
    ("L", "Large"),
    )
TYPES = (
    ("R", "Regular"),
    ("S", "Sicilian"),
    )

class Toppings(models.Model):
    topping = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f"{self.topping}"


class ExtraPricing(models.Model):
    num_extra = models.CharField(max_length=20, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.num_extra} adds {self.price}"
    
class Pizza(models.Model):
    type = models.CharField(max_length=1, choices=TYPES)
    size = models.CharField(max_length=1, choices=SIZES)
    toppings = models.ManyToManyField(Toppings, blank=True, related_name="pizza_topping")
    plainPrice = models.DecimalField(max_digits=5, decimal_places=2)
    plusOnePrice = models.DecimalField(max_digits=5, decimal_places=2)
    plusTwoPrice = models.DecimalField(max_digits=5, decimal_places=2)
    plusThreePrice = models.DecimalField(max_digits=5, decimal_places=2)
    specialPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"[{self.size}][{self.type}]: ${self.plainPrice} ${self.plusOnePrice} ${self.plusTwoPrice} ${self.plusThreePrice} ${self.specialPrice}"

class Extras(models.Model):
    type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} ${self.price}"

class Sub (models.Model):
    type = models.CharField(max_length=64, blank=False)
    extras = models.ManyToManyField(Extras, blank=True, related_name="sub_extras")
    smPrice = models.DecimalField(max_digits=5, decimal_places=2)
    lgPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} Small: ${self.smPrice} Large: ${self.lgPrice}"

class Salad(models.Model):
    type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.salad}"

class Pasta(models.Model):
    type = models.CharField(max_length=30, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pasta}"

class Platter(models.Model):
    type = models.CharField(max_length=30, blank=False)
    smPrice = models.DecimalField(max_digits=5, decimal_places=2)
    lgPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} ${self.smPrice} ${self.lgPrice}"

                     

