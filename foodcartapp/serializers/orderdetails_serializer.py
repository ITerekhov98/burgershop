from rest_framework import serializers

from foodcartapp.models import OrderPosition


class OrderPositionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        orderdetails = OrderPosition.objects.create(**validated_data)
        return orderdetails
