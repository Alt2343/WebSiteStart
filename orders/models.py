from django.db import models
from django.utils import timezone
from shop.models import Product
class Order(models.Model):
    ORDER_STATUS = [
        ('created', 'Создан'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    DELIVERY_METHODS = [
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    ]
    first_name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    email = models.EmailField(verbose_name='Email')
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHODS, default='delivery', verbose_name='Способ доставки')
    address = models.TextField(verbose_name='Адрес доставки', blank=True)
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', blank=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    delivery_notes = models.TextField(verbose_name='Примечания к доставке', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='created', verbose_name='Статус')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    # Добавляем поля для безналичной оплаты
    stripe_id = models.CharField(max_length=250, blank=True, verbose_name='ID платежа Stripe')
    # Поля для комментариев администратора
    admin_notes = models.TextField(verbose_name='Заметки администратора', blank=True)
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name='Номер для отслеживания',help_text='Заполняется после оплаты для отслеживания посылки')
    order_number = models.CharField(max_length=20,unique=True,editable=False,verbose_name='Номер заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Генерация номера заказа по дате"""
        today = timezone.now()

        # Формат: ГОДМЕСЯЦДЕНЬ-ПОРЯДКОВЫЙНОМЕР
        date_part = today.strftime('%Y%m%d')

        # Находим количество заказов за сегодня
        today_orders = Order.objects.filter(created__date=today.date()).count()
        sequence_number = today_orders + 1

        return f"{date_part}-{sequence_number:04d}"

    def __str__(self):
        return f'Заказ {self.order_number}'

    def get_total_cost(self):
        total = 0
        for item in self.items.all():
            if item.price and item.quantity:
                total += item.price * item.quantity
        return total

    def get_customer_info(self):
        """Получить основную информацию о клиенте"""
        return f"{self.first_name} {self.last_name}, тел.: {self.phone}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name}'

    def get_cost(self):
        if self.price and self.quantity:
            return self.price * self.quantity
        return 0




