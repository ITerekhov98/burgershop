from django.conf import settings
from django.contrib import admin
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.exceptions import ObjectDoesNotExist
from .models import Product
from .models import ProductCategory
from .models import Restaurant
from .models import RestaurantMenuItem
from .models import Purchase, Order


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ]
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide'
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html('<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>', edit_url=edit_url, src=obj.image.url)
    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        Используем кешированные объекты чтобы избежать 
        многократных запросов к базе данных 
        '''
        field = super().formfield_for_foreignkey(db_field, request)
        if db_field.name == "product" and hasattr(self, "cached_products"):
            field.choices = self.cached_products
        return field        

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('phonenumber', 'created_at',)
    fields = (
        'phonenumber',
        'firstname',
        'lastname',
        'address',
        'payment',
        'restaurant',
        'called_at',
        'delivered_at',
        'comment',
        'created_at'
    )
    readonly_fields = ('created_at',)
    inlines = (PurchaseInline,)

    def get_formsets_with_inlines(self, request, obj=None):
        '''
        Достаём и сохраняем продукты, чтобы использовать их при рендере PurchaseInline
        '''
        for inline in self.get_inline_instances(request, obj):
            inline.cached_products = [(i.pk, str(i)) for i in Product.objects.all()]
            yield inline.get_formset(request, obj), inline

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        Если в заказе уже присутствуют покупки, предопределяём выбор ресторанов
        исходя из наличия в них нужных позиций
        '''
        if not db_field.name == "restaurant":
            return
        try:
            order_id = request.resolver_match.kwargs.get('object_id')
            order = Order.objects.filter(id=order_id).with_available_restaurants()[0]
        except ObjectDoesNotExist:
            return
        available_restaurants_ids = [restaurant.id for restaurant in order.available_restaurants]
        kwargs["queryset"] = Restaurant.objects.filter(
            id__in=available_restaurants_ids
        )
        return super().formfield_for_foreignkey(
            db_field, request,
            **kwargs
        )

    def response_post_save_change(self, request, obj):
        '''
        Возвращаем на страницу менеджера после сохранения заказа,
        если запрос был сделан с неё
        '''
        res = super().response_post_save_change(request, obj)
        if "next" in request.GET:
            url_allow = url_has_allowed_host_and_scheme(
                request.GET['next'],
                settings.ALLOWED_HOSTS
            )
            if url_allow:
                return HttpResponseRedirect(request.GET['next'])
        return res

    def save_formset(self, request, form, formset, change):
        '''
        При указании готовящего ресторана меняем статус заказа на PROCCESSED
        Если менеджер не указал цену для товара, рассчитываем её автоматически
        '''
        order = form.save(commit=False)
        if order.restaurant and order.status == 'UN':
            order.status = 'P'
        order.save()

        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.price:
                instance.price = instance.product.price
            instance.save()
        formset.save()

