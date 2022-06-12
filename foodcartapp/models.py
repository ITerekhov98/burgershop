from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=1000,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def with_cost(self):
        return self.exclude(status='D') \
                   .annotate(
                   cost=Sum(F('purchases__price') * F('purchases__quantity'))) \
                   .order_by('-created_at')


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
    address = models.TextField('адрес', db_index=True, max_length=200)
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
    comment = models.TextField('комментарий', max_length=200, blank=True)
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
        related_name='products',
        verbose_name='блюдо',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[MinValueValidator(0), MaxValueValidator(20)]
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
        return f"{self.product} - {self.quantity}шт."
