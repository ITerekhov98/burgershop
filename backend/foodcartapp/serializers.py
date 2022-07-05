from rest_framework.serializers import ListField, ModelSerializer

from .models import Product, Order, Purchase


class PurchaseSerializer(ModelSerializer):
    class Meta:
        fields = ['quantity', 'product']
        model = Purchase 


class OrderSerializer(ModelSerializer):
    products = ListField(child=PurchaseSerializer(), allow_empty=False, write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'phonenumber', 'firstname', 'lastname', 'address', 'products']