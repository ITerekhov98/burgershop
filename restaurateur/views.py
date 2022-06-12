import requests
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from geopy import distance

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from geolocation.models import PlaceLocation
from django.conf import settings


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
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

        return render(request, "login.html", context={
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
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def get_places_coordinats(places):
    addresses = [place.address for place in places]
    saved_locations = PlaceLocation.objects.filter(address__in=addresses)
    saved_addresses = [location.address for location in saved_locations]
    serialized_coordinats = {}

    for address in addresses:
        if address not in saved_addresses:
            coordinats = fetch_coordinates(settings.YANDEX_API_TOKEN, address)
            if coordinats:
                PlaceLocation.objects.create(
                    address=address,
                    longitude=float(coordinats[0]),
                    latitude=float(coordinats[1])
                )
                serialized_coordinats[address] = coordinats

    for place in saved_locations:
        if place.address not in serialized_coordinats:
            serialized_coordinats[place.address] = (
                str(place.longitude),
                str(place.latitude)
            )

    return serialized_coordinats


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.with_cost() \
                          .prefetch_related('purchases__product') \
                          .select_related('restaurant') \
                          .order_by('-status')

    restaurant_menu_items = RestaurantMenuItem.objects.all() \
                                                      .select_related('product') \
                                                      .select_related('restaurant')
    orders_coordinats = get_places_coordinats(orders)
    restaurants_coordinates = get_places_coordinats(Restaurant.objects.all())
    for order in orders:
        order.coordinates = orders_coordinats.get(order.address)
        order.available_restaurants = []
        for purchase in order.purchases.all():
            res = [item.restaurant for item in restaurant_menu_items
                   if item.product == purchase.product and item.availability]
            if not order.available_restaurants:
                order.available_restaurants.extend(res)
            else:
                order.available_restaurants = [item for item in order.available_restaurants 
                                               if item in res]
        if order.coordinates:
            for restaurant in order.available_restaurants:
                restaurant_coordinates = restaurants_coordinates[restaurant.address]
                restaurant.distance = distance.distance(
                    order.coordinates,
                    restaurant_coordinates).km
                restaurant.readable_distance = f' {restaurant.distance:.4f} км'
            order.available_restaurants = sorted(
                order.available_restaurants,
                key=lambda x: x.distance
            )
    return render(
        request,
        template_name='order_items.html',
        context={'order_items': orders}
    )
