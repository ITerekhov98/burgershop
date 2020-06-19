from django.urls import path

from foodcartapp.RESTviews.CityRestView import city_list_api
from foodcartapp.RESTviews.OrderRestView import order_list_api
from foodcartapp.RESTviews.ProductRestView import product_list_api
from foodcartapp.RESTviews.BannersView import banners_list_api
from foodcartapp.RESTviews.UserRestView import customer_signup_api
from foodcartapp.views.RestaurantViews import RestaurantListView
from foodcartapp.views.OrderViews import OrderListView
from foodcartapp.views.ProductViews import ProductListView, AddProductView, UpdateProductView, DeleteProductView
from foodcartapp.views.AuthViews import LoginView, LogoutView

app_name = "foodcartapp"

urlpatterns = [

    path('products/', ProductListView.as_view(), name="ProductsView"),
    path('addproduct/', AddProductView.as_view(), name="AddProductView"),
    path('<int:pk>/editProduct/', UpdateProductView.as_view(), name="UpdateProductView"),
    path('<int:pk>/deleteProduct/', DeleteProductView.as_view(), name="DeleteProductView"),

    path('restaurants/', RestaurantListView.as_view(), name="RestaurantView"),

    path('orders/', OrderListView.as_view(), name="OrderListView"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="Logout"),

    path('api/products/', product_list_api, name="ProductListAPI"),

    path('api/banners/', banners_list_api, name="BannersListAPI"),

    path('api/cities/', city_list_api, name="CityListAPI"),


    path('api/order/', order_list_api, name="OrderListAPI"),

    path('api/user_signup/', customer_signup_api, name="UserSignupAPI"),

]
