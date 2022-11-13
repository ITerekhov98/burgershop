from django.db import models
from django.utils import timezone


class PlaceLocation(models.Model):
    address = models.CharField('адрес', unique=True, max_length=200)
    longitude = models.FloatField('долгота', blank=True, null=True)
    latitude = models.FloatField('широта', blank=True, null=True)
    created_at = models.DateTimeField(
        'дата и время заказа',
        default=timezone.now,
        db_index=True
    )
