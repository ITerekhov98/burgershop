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


class Location(models.Model):  # FIXME выпилить?
    name = models.CharField('', max_length=50, help_text='')  # FIXME
    city = models.ForeignKey(City, verbose_name='город', on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = '???'  # FIXME
        verbose_name_plural = '???'  # FIXME


class CustomUser(models.Model):  # FIXME переименовать в Customer ?
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
        CustomUser.objects.create(user=instance)


class Hotel(models.Model):   # FIXME переименовать в ресторан ?
    name = models.CharField('название', max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='hotels')  # FIXME
    hoteladmin = models.ForeignKey(CustomUser, verbose_name='администратор', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='administrated_hotels')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = '???'  # FIXME
        verbose_name_plural = '???'  # FIXME


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    full_price = models.DecimalField('цена', max_digits=8, decimal_places=2)  # FIXME переименовать поле в price
    availabilty = models.BooleanField('в продаже', default=True, db_index=True)  # FIXME опечатка в названии
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    category = models.CharField('категория', max_length=50)  # FIXME заменить на choices
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='products')  # FIXME

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, verbose_name='заказчик', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='orders')
    status = models.SmallIntegerField('статус', default=1, db_index=True)  # FIXME определить choices и их названия
    order_time = models.DateTimeField('заказано', default=timezone.now, db_index=True)
    delivery_time = models.DateTimeField('доставлено', blank=True, null=True, db_index=True)
    amount = models.DecimalField('стоимость', max_digits=15, decimal_places=2)
    order_type = models.SmallIntegerField('тип заказа', default=1, db_index=True)  # FIXME определить choices и их названия

    def __str__(self):
        return f"{self.customer} status:{self.status} order time:{self.order_time}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderDetails(models.Model):  # FIXME переименовать в OrderPosition ?
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE, related_name='order_positions')
    quantity = models.DecimalField('количество', max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return f"{self.product} x{self.quantity} for order #{self.order_id}"

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'позиции заказов'
