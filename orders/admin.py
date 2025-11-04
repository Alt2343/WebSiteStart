from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'phone', 'delivery_method', 'status', 'paid', 'created']
    list_filter = ['status', 'paid', 'delivery_method']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone']
    readonly_fields = ['order_number', 'created', 'updated']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'status', 'paid', 'created', 'updated')
        }),
        ('Данные клиента', {
            'fields': ('first_name', 'last_name', 'phone', 'email')
        }),
        ('Доставка', {
            'fields': ('delivery_method', 'address', 'city','tracking_number')
        }),
    )


admin.site.register(Order, OrderAdmin)