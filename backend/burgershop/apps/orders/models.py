from django.db import models
from django.db.models import F, Sum
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from burgershop.apps.restaurants.models import RestaurantMenuItem, Restaurant
from burgershop.apps.products.models import Product

class OrderQuerySet(models.QuerySet):
    def with_available_restaurants(self):
        restaurant_menu_items = RestaurantMenuItem.objects.filter(availability=True) \
                                                  .select_related('product') \
                                                  .select_related('restaurant')
        affordable_restaurants = {}
        for item in restaurant_menu_items:
            if not affordable_restaurants.get(item.product):
                affordable_restaurants[item.product] = set()
            affordable_restaurants[item.product].add(item.restaurant)
        for order in self:
            products = [purchase.product for purchase in order.purchases.all()]
            all_affordable_restaurants = [
                affordable_restaurants.get(product, set()) for product in products
            ]
            order.available_restaurants = list(
                set.intersection(*all_affordable_restaurants)
            )
        return self
   
    def with_cost(self):
        return self.exclude(status='D') \
                   .annotate(
                   cost=Sum(F('purchases__price') * F('purchases__quantity'))) \
                   .order_by('-created_at')
    
    def copy_from(self, old_order):
        new_order = self.get(pk=old_order.pk)
        new_order.pk = None
        new_order.comment = f'Копия заказа {old_order.pk}'
        new_order.save()

        purchases = old_order.purchases.all()
        for purchase in purchases:
            purchase.pk = None
            purchase.order = new_order
        Purchase.objects.bulk_create(purchases)
            


class Order(models.Model):
    UNPROCCESSED = 'UN'
    PROCCESSED = 'P'
    ON_THE_WAY = 'OTW'
    DONE = 'D'
    STATUSES = (
        (UNPROCCESSED, 'Необработан'),
        (PROCCESSED, 'Готовится'),
        (ON_THE_WAY, 'В пути'),
        (DONE, 'Завершён')
    )
    PAYMENT_METHODS = (
        ('CASH', 'Наличными'),
        ('CARD', 'Онлайн')
    )
    phonenumber = PhoneNumberField('номер телефона', db_index=True)
    firstname = models.CharField('имя покупателя', max_length=50)
    lastname = models.CharField(
        'фамилия покупателя',
        max_length=50,
        blank=True
    )
    address = models.CharField('адрес', db_index=True, max_length=200)
    created_at = models.DateTimeField(
        'дата и время заказа',
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        'дата и время потверждения',
        db_index=True,
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        'дата и время доставки',
        db_index=True,
        blank=True,
        null=True
    )
    status = models.CharField(
        'статус',
        max_length=10,
        choices=STATUSES,
        default=UNPROCCESSED,
        db_index=True
    )
    comment = models.TextField('комментарий', blank=True)
    payment = models.CharField(
        'метод оплаты',
        max_length=5,
        choices=PAYMENT_METHODS,
        db_index=True
    )
    
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='orders',
        verbose_name='готовящий ресторан',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.phonenumber}'


class Purchase(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='purchases',
        verbose_name='заказ',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='purchases',
        verbose_name='блюдо',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True
    )

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'

    def __str__(self):
        return f"{self.product} - {self.quantity} шт"

