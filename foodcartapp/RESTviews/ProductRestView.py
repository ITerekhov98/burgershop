from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.models import Product
from foodcartapp.serializers.product_serializer import ProductSerializer


@api_view(['GET'])
def product_list_api(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
    else:
        # FIXME стоит проверить на права администратора и выдать только товары его собственного магазина
        products = Product.objects.active()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
