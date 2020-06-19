import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.serializers.order_serializer import OrderSerializer
from foodcartapp.serializers.orderdetails_serializer import OrderItemSerializer


@api_view(['POST'])
def order_list_api(request):
    order_data = {
        'customer_id': request.user.id,
        'order_time': datetime.datetime.now(),
        'amount': request.data['amount'],
    }

    products = request.data.pop('products')
    order_serializer = OrderSerializer(data=order_data)

    if order_serializer.is_valid():
        order = order_serializer.save()
        for product in products:
            orderdetails_data = {
                'product_id': product['id'],
                'quantity': product['quantity'],
                'order_id': order.id,
            }
            orderdetail_serializer = OrderItemSerializer(data=orderdetails_data)
            if orderdetail_serializer.is_valid():
                orderdetail_serializer.save()

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
