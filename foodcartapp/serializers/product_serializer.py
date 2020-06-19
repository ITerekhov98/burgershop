from rest_framework import serializers

from foodcartapp.serializers.restaurant_serializer import RestaurantSerializer


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    availability = serializers.BooleanField(default=True)
    image = serializers.URLField(source='image.url', read_only=True)
    special_status = serializers.BooleanField(default=False)
    category = serializers.CharField(max_length=50)
    restaurant = RestaurantSerializer(many=False)
