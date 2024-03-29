from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from geopy import distance

from burgershop.apps.products.models import Product
from burgershop.apps.restaurants.models import Restaurant
from burgershop.apps.orders.models import Order

from burgershop.apps.geolocation.services import get_places_coordinats
from .forms import Login



class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "restaurateur/login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "restaurateur/login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [
            availability[restaurant.id] for restaurant in restaurants
        ]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="restaurateur/products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurateur/restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.with_cost() \
                          .prefetch_related('purchases__product') \
                          .select_related('restaurant') \
                          .order_by('-status') \
                          .with_available_restaurants()
    orders_coordinats = get_places_coordinats(
        [order.address for order in orders]
    )
    restaurants_coordinates = get_places_coordinats(
        Restaurant.objects.values_list('address', flat=True)
    )
    for order in orders:
        order.coordinates = orders_coordinats.get(order.address)
        if not order.coordinates:
            continue

        order.readable_distance = {}
        for restaurant in order.available_restaurants:
            restaurant_coordinates = restaurants_coordinates[restaurant.address]
            restaurant.distance = distance.distance(
                order.coordinates,
                restaurant_coordinates).kilometers
            order.readable_distance[restaurant.name] = f' {restaurant.distance:.4f} км'
        order.available_restaurants = sorted(
            order.available_restaurants,
            key=lambda x: x.distance
        )
    return render(
        request,
        template_name='restaurateur/order_items.html',
        context={'order_items': orders}
    )
