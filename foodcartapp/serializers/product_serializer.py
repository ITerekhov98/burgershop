from rest_framework import serializers

from foodcartapp.models import Restaurant, Product


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
