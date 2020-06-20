from django.contrib import admin

from .models import City, Restaurant, Product

admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(Product)
