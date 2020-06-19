from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.models import City
from foodcartapp.serializers.city_serializer import CitySerializer


@api_view(['GET'])
def city_list_api(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)
