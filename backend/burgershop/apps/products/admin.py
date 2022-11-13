from django.contrib import admin
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.html import format_html
from burgershop.apps.restaurants.models import Restaurant
from burgershop.apps.restaurants.admin import RestaurantMenuItemInline

from .models import Product, ProductCategory


class ProductsFilterByRestaurant(admin.SimpleListFilter):
    title = 'Доступны в Ресторане'
    parameter_name = 'restaurant_pk'

    def lookups(self, request, model_admin):
        queryset = Restaurant.objects.all()
        restaurants = {
            (
                str(restaurant.pk),
                restaurant.name,
            )
            for restaurant in queryset
        }
        return restaurants

    def queryset(self, request, queryset):
        restaurant_pk = self.value()
        if restaurant_pk:
            return queryset.filter(
                menu_items__restaurant__pk=restaurant_pk,
                menu_items__availability=True
            ).distinct()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'get_image_list_preview',
        'name',
        'category',
        'price',
    )
    list_display_links = (
        'name',
    )
    list_filter = (
        'category',
        ProductsFilterByRestaurant,
    )
    search_fields = (
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    )

    inlines = (
        RestaurantMenuItemInline,
    )
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

    readonly_fields = (
        'get_image_preview',
    )

    class Media:
        css = {
            "all": (
                static("admin/products.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html(
            '<img src="{url}" style="max-height: 200px;"/>',
            url=obj.image.url
        )
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:products_product_change', args=(obj.id,))
        return format_html(
            '<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>',
            edit_url=edit_url, src=obj.image.url
        )
    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass