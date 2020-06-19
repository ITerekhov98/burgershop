import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.models import Order
from foodcartapp.serializers.order_serializer import OrderSerializer
from foodcartapp.serializers.orderdetails_serializer import OrderItemSerializer
from foodcartapp.serializers.product_serializer import ProductSerializer


@api_view(['POST'])
def order_list_api(request):
    if request.method == 'POST':
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


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail_api(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.query_params)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
