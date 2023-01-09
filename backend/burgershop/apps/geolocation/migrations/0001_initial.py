# Generated by Django 3.2 on 2022-06-11 13:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, unique=True, verbose_name='адрес')),
                ('longitude', models.FloatField(verbose_name='долгота')),
                ('latitude', models.FloatField(verbose_name='широта')),
                ('category', models.CharField(choices=[('RES', 'Ресторан'), ('OR', 'заказ'), ('OTH', 'другое')], max_length=5, verbose_name='категория')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='дата и время заказа')),
            ],
        ),
    ]