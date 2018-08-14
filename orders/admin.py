from django.contrib import admin

# Register your models here.
from .models import Pizza, Toppings, Extras, Sub, Salad, Pasta, \
    Platter, ExtraPricing

admin.site.register(Pizza)
admin.site.register(Toppings)
admin.site.register(Extras)
admin.site.register(Sub)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(Platter)
admin.site.register(ExtraPricing)
