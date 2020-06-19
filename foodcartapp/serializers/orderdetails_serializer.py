from rest_framework import serializers

from foodcartapp.models import OrderItem


class OrderItemSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        orderdetails = OrderItem.objects.create(**validated_data)
        return orderdetails
