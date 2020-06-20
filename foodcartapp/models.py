from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='учётка', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='customer', help_text='если зарегистрирован на сайте')
    phone_number = models.CharField('телефон', max_length=10)
    address = models.CharField('адрес', max_length=256)

    def __str__(self):
        return f"{self.user.username} {self.user.get_full_name()} {self.phone_number}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    city = models.ForeignKey(City, verbose_name='город', on_delete=models.CASCADE, related_name='restaurants')
    admin = models.ForeignKey(User, verbose_name='администратор', on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='administrated_restaurants')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(availability=True)


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    price = models.DecimalField('цена', max_digits=8, decimal_places=2)
    availability = models.BooleanField('в продаже', default=True, db_index=True)
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    category = models.CharField('категория', max_length=50)  # FIXME заменить на choices или отдельную модель данных
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='products')

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Order(models.Model):
    NEW_ORDER = 1
    CONFIRMED_ORDER = 2
    COOKING = 3
    ON_THE_WAY = 4
    DELIVERED_ORDER = 5
    CANCELLED = 6
    STATUS_CHOICES = (
        (NEW_ORDER, 'новый'),
        (CONFIRMED_ORDER, 'подтверждён'),
        (COOKING, 'готовится'),
        (ON_THE_WAY, 'в пути'),
        (DELIVERED_ORDER, 'доставлен'),
        (CANCELLED, 'отменён'),
    )

    CASH_ON_DELIVERY = 1
    PAYMENT_CHOICES = (
        (CASH_ON_DELIVERY, 'наличными после доставки'),
    )


    customer = models.ForeignKey(Customer, verbose_name='заказчик', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='orders')
    status = models.SmallIntegerField('статус', default=NEW_ORDER, db_index=True, choices=STATUS_CHOICES)
    order_time = models.DateTimeField('заказано', default=timezone.now, db_index=True)
    delivery_time = models.DateTimeField('доставлено', blank=True, null=True, db_index=True)
    amount = models.DecimalField('стоимость', max_digits=15, decimal_places=2)
    payment_type = models.SmallIntegerField('тип заказа', default=CASH_ON_DELIVERY, db_index=True, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"{self.customer} status:{self.status} order time:{self.order_time}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE, related_name='orders_items')
    quantity = models.DecimalField('количество', max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.product} x{self.quantity} for order #{self.order_id}"

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'позиции заказов'
