from django.db import models

# Create your models here.
class PizzaType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.type}"

class Toppings(models.Model):
    topping = models.CharField(max_length=20, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Add {self.topping} for {self.price}"

class Pizza(models.Model):
    SIZES = (
        ("S", "Small"),
        ("L", "Large"),
        )
    type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name="pizza_style")
    size = models.CharField(max_length=1, choices=SIZES)
    toppings = models.ManyToManyField(Toppings, blank=True, related_name="pizza_topping")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} ({self.size} (with {self.toppings})) costs {self.price}"

class Extras(models.Model):
    extras = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Add {self.extra} for {self.price}"

class Sub (models.Model):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
        )
    type = models.CharField(max_length=64, blank=False)
    size = models.CharField(max_length=1, choices=SIZES)
    extras = models.ManyToManyField(Extras, blank=True, related_name="sub_extras")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.size} {self.type} (with {self.extras})"

class Salad(models.Model):
    salad = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.salad} costs {self.price}"

class Pasta(models.Model):
    pasta = models.CharField(max_length=30, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pasta} costs {self.price}"

class Platter(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
        )
    size = models.CharField(max_length=1, choices=SIZES)
    platter = models.CharField(max_length=30, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.size} {self.platter} costs {self.price}"

                     

