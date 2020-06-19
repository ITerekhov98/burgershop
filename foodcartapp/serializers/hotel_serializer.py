from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Hotel


class HotelSerializer(ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        return Hotel.objects.create(**validated_data)
