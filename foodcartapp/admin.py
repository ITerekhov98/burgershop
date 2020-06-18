from django.contrib import admin

from .models import City, Location, CustomUser, Hotel, Product, Order, OrderDetails

admin.site.register(City)
admin.site.register(Location)
admin.site.register(CustomUser)
admin.site.register(Hotel)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetails)
