from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework.response import Response

from .serializers import OrderSerializer
from .models import Order, Purchase


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    registered_order = Order.objects.create(
        phonenumber=serializer.validated_data.get('phonenumber'),
        firstname=serializer.validated_data.get('firstname'),
        lastname=serializer.validated_data.get('lastname'),
        address=serializer.validated_data.get('address'),
    )
    Purchase.objects.bulk_create(
        [Purchase(
            order=registered_order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price,)
            for item in serializer.validated_data['products']]
    )
    serializer = OrderSerializer(registered_order)
    return Response(serializer.data, status=201)

