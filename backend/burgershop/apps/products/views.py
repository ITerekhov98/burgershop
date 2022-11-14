from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import generics

from .models import Product
from .serializers import ProductsSerializer

def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class ProductsList(generics.ListAPIView):
    '''Получение списка продуктов'''
    queryset = Product.objects.select_related('category').available()
    serializer_class = ProductsSerializer
