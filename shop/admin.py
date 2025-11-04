from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'in_stock', 'created_at']
    list_filter = ['category', 'in_stock', 'brand']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    # Показываем превью фото в админке
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.main_image:
            return mark_safe(f'<img src="{obj.main_image.url}" width="100" />')
        return "Нет фото"

    image_preview.short_description = 'Превью главного фото'