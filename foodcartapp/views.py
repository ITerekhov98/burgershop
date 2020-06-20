from django.templatetags.static import static
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

from .models import City
from .models import Product
from .models import Restaurant


@api_view(['GET'])
def banners_list_api(request):
    # FIXME move data to db?
    return Response([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ])


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


@api_view(['GET'])
def city_list_api(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source='image.url', read_only=True)
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'special_status', 'category', 'image', 'restaurant']


@api_view(['GET'])
def product_list_api(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
    else:
        # FIXME стоит проверить на права администратора и выдать только товары его собственного магазина
        products = Product.objects.active()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def register_order(request):
    # TODO это лишь заглушка
    return JsonResponse({})
