import phonenumbers
from phonenumbers import NumberParseException

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order, Purchase


class OrderValidationError(Exception):
    def __init__(self, report):
        self.report = report


def check_phonenumber(number):
    try:
        parsed_number = phonenumbers.parse(number)
    except NumberParseException:
        return False
    return phonenumbers.is_valid_number(parsed_number)


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


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })

def validate_order_data(serialized_order):
    required_fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']
    report = None

    missing_fields = set(required_fields).difference(serialized_order.keys())
    fields_with_empty_values = [field for field, value in serialized_order.items() if not value]

    if missing_fields:
        report = f"{', '.join(field for field in missing_fields)}: обязательные поля"

    elif not isinstance(serialized_order['firstname'], str):
        report = 'firstname: Not a valid string.'

    elif fields_with_empty_values:
        report = f"{', '.join(field for field in fields_with_empty_values)}: Эти поля не могут быть пустыми"

    elif not isinstance(serialized_order['products'], list):
        report = "products: Ожидался list со значениями, но был получен 'str'."

    elif not check_phonenumber(serialized_order['phonenumber']):
        report = "phonenumber: Введен некорректный номер телефона."
    
    else:
        ordered_products_ids = set([item['product'] for item in serialized_order['products']])
        existing_products_ids = set(Product.objects.filter(pk__in=ordered_products_ids).values_list('id', flat=True))
        if ordered_products_ids != existing_products_ids:
            unexisting_products_ids = ordered_products_ids.difference(existing_products_ids)
            report = f"products: Недопустимый первичный ключ: {' '.join(str(pk) for pk in unexisting_products_ids)}"

    if report:
        raise OrderValidationError(report)
    return
 

@api_view(['POST'])
def register_order(request):
    serialized_order = request.data
    try:
        validate_order_data(serialized_order)
    except OrderValidationError as err:
        return Response({'error': err.report}, status=status.HTTP_400_BAD_REQUEST)

    registered_order = Order.objects.create(
        phonenumber = serialized_order.get('phonenumber'),
        firstname = serialized_order.get('firstname'),
        lastname = serialized_order.get('lastname'),
        address = serialized_order.get('address'),
    )
    Purchase.objects.bulk_create(
        [Purchase(
            order=registered_order,
            product_id=item['product'],
            count=item['quantity']) for item in serialized_order['products']]
    )
    return Response({})
