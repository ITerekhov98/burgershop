from django.contrib import admin

from .models import City, Location, Customer, Hotel, Product, Order, OrderItem

admin.site.register(City)
admin.site.register(Location)
admin.site.register(Customer)
admin.site.register(Hotel)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
