from django.urls import include
from django.urls import path

from burgershop.apps.products.views import banners_list_api, product_list_api

urlpatterns = [
    path('products/', product_list_api),
    path('banners/', banners_list_api),
    path('order/', include('burgershop.apps.orders.urls')),
]
