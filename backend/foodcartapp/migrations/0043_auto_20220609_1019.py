# Generated by Django 3.2 on 2022-06-09 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20220606_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('UN', 'Необработан'), ('C', 'Готовится'), ('OTW', 'В пути'), ('D', 'Завершён')], db_index=True, default='UN', max_length=10, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
        ),
    ]
