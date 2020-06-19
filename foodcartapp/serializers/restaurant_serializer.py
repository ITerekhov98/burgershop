from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Restaurant


class RestaurantSerializer(ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)
