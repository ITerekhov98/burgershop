from rest_framework import serializers

from foodcartapp.serializers.hotel_serializer import HotelSerializer


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    full_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    availabilty = serializers.BooleanField(default=True)
    image = serializers.URLField(source='image.url', read_only=True)
    special_status = serializers.BooleanField(default=False)
    category = serializers.CharField(max_length=50)
    hotel = HotelSerializer(many=False)
