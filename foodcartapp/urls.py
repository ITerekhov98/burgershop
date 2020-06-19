from django.urls import path

from foodcartapp.RESTviews.CityRestView import city_list_api
from foodcartapp.RESTviews.OrderRestView import order_list_api
from foodcartapp.RESTviews.ProductRestView import product_list_api
from foodcartapp.RESTviews.BannersView import banners_list_api
from foodcartapp.RESTviews.UserRestView import customer_signup_api
from foodcartapp.views.CityViews import city_list_view, AddCityView, UpdateCityView, DeleteCityView
from foodcartapp.views.RestaurantViews import restaurant_list_view, DeleteRestaurantView, UpdateRestaurantView, AddRestaurantView
from foodcartapp.views.OrderViews import order_list_view
from foodcartapp.views.ProductViews import product_list_view, AddProductView, UpdateProductView, DeleteProductView
from foodcartapp.views.AuthViews import LoginView, LogoutView, SignUpView

app_name = "foodcartapp"

urlpatterns = [

    path('products/', product_list_view.as_view(), name="ProductsView"),
    path('addproduct/', AddProductView.as_view(), name="AddProductView"),
    path('<int:pk>/editProduct/', UpdateProductView.as_view(), name="UpdateProductView"),
    path('<int:pk>/deleteProduct/', DeleteProductView.as_view(), name="DeleteProductView"),

    path('restaurants/', restaurant_list_view.as_view(), name="RestaurantView"),
    path('addrestaurant/', AddRestaurantView.as_view(), name="AddRestaurantView"),
    path('<int:pk>/editRestaurant/', UpdateRestaurantView.as_view(), name="UpdateRestaurantView"),
    path('<int:pk>/deleteRestaurant/', DeleteRestaurantView.as_view(), name="DeleteRestaurantView"),


    path('cities/', city_list_view.as_view(), name="CitiesView"),
    path('addcity/', AddCityView.as_view(), name="AddCityView"),
    path('<int:pk>/editCity/', UpdateCityView.as_view(), name="UpdateCityView"),
    path('<int:pk>/deleteCity/', DeleteCityView.as_view(), name="DeleteCityView"),

    path('orders/', order_list_view.as_view(), name="OrderListView"),

    path('login/', LoginView.as_view(), name="Login"),
    path('logout/', LogoutView.as_view(), name="Logout"),
    path('sign_up/', SignUpView.as_view(), name="Signup"),

    path('api/products/', product_list_api, name="ProductListAPI"),

    path('api/banners/', banners_list_api, name="BannersListAPI"),

    path('api/cities/', city_list_api, name="CityListAPI"),


    path('api/order/', order_list_api, name="OrderListAPI"),

    path('api/user_signup/', customer_signup_api, name="UserSignupAPI"),

]
