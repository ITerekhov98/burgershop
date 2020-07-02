from django.urls import path
from django.shortcuts import render, redirect

from .views import view_restaurants
from .views import view_products
from .views import LoginView, LogoutView

app_name = "restaurateur"

urlpatterns = [
    path('', lambda request: redirect('restaurateur:ProductsView')),

    path('products/', view_products, name="ProductsView"),

    path('restaurants/', view_restaurants, name="RestaurantView"),

    # TODO заглушка для нереализованного функционала
    path('orders/', render, kwargs={
        'template_name': 'order_items.html',
    }, name="OrderListView"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
