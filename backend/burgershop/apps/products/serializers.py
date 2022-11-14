from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from .models import Product, ProductCategory


class CategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name'
        )

class ProductsSerializer(ModelSerializer):
    category = CategorySerializer()

    def get_category(self, obj):
        return {
            'id': obj.category.id,
            'name': obj.category.name
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url
        representation['restaurant'] = {
            'id': instance.id,
            'name': instance.name
        }
        return representation

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'special_status',
            'description',
            'category',
            'image',
        )
