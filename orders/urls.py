from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("menu", views.menu_view, name="menu"),
    path("shoppingCart", views.shoppingCart, name="shoppingCart"),
    path("emptyCart", views.emptyCart, name="emptyCart"),
    path("orderOnline", views.orderOnline, name="orderOnline"),
    path("placeOrder", views.placeOrder_view, name="placeOrder")
]
