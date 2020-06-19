from django.contrib import admin

from .models import City, Customer, Restaurant, Product, Order, OrderItem

admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
