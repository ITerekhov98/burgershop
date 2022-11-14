from django.urls import include
from django.urls import path

from burgershop.apps.products.views import banners_list_api, ProductsList

urlpatterns = [
    path('products/', ProductsList.as_view()),
    path('banners/', banners_list_api),
    path('order/', include('burgershop.apps.orders.urls')),
]
