from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart
from shop.models import Product


def order_create(request):
    """Создание нового заказа"""
    cart = Cart(request)

    if request.method == 'POST':
        # Создаем заказ из данных формы
        order = Order(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
            delivery_method=request.POST.get('delivery_method', 'delivery'),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
        )
        order.save()

        # Добавляем товары из корзины в заказ
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Очищаем корзину
        cart.clear()

        messages.success(request, f'Ваш заказ №{order.order_number} успешно создан!')
        return redirect('orders:order_created', order_id=order.id)  # ← Добавьте 'orders:'

    # GET запрос - показываем форму
    return render(request, 'orders/order_create.html', {'cart': cart})


def order_created(request, order_id):
    """Страница успешного создания заказа"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})


def order_lookup(request):
    """Поиск заказа по номеру"""
    order = None
    order_number = ""

    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip()
        if order_number:
            try:
                order = Order.objects.get(order_number=order_number)
            except Order.DoesNotExist:
                messages.error(request, 'Заказ с таким номером не найден')

    return render(request, 'orders/order_lookup.html', {
        'order': order,
        'order_number': order_number
    })


def order_detail(request, order_id):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})