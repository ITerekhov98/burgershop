from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'


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
    category = models.CharField('категория', max_length=50)  # TODO заменить на choices или отдельную модель данных
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='products')
    ingridients = models.CharField('ингредиенты', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
