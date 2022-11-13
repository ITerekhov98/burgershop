from django.urls import path

from .views import register_order


app_name = "orders"

urlpatterns = [
    path('', register_order),
]