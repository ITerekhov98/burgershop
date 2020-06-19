from django.urls import path

from foodcartapp.RESTviews.CityRestView import city_list_api
from foodcartapp.RESTviews.OrderRestView import order_list_api
from foodcartapp.RESTviews.ProductRestView import product_list_api
from foodcartapp.RESTviews.BannersView import banners_list_api
from foodcartapp.RESTviews.UserRestView import customer_signup_api


app_name = "foodcartapp"

urlpatterns = [
    path('products/', product_list_api, name="ProductListAPI"),

    path('banners/', banners_list_api, name="BannersListAPI"),

    path('cities/', city_list_api, name="CityListAPI"),


    path('order/', order_list_api, name="OrderListAPI"),

    path('user_signup/', customer_signup_api, name="UserSignupAPI"),

]
