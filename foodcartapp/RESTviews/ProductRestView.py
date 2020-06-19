from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.models import Product
from foodcartapp.serializers.product_serializer import ProductSerializer


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
