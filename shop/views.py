from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from . import models
from .models import Category, Product


# Функция для главной страницы
def home(request):
    categories = Category.objects.all()

    # Добавляем фильтрацию товаров по категории
    category_slug = request.GET.get('category')
    if category_slug:
        featured_products = Product.objects.filter(
            category__slug=category_slug,
            in_stock=True
        )[:8]
        selected_category = get_object_or_404(Category, slug=category_slug)
    else:
        featured_products = Product.objects.filter(in_stock=True)[:8]
        selected_category = None

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'selected_category': selected_category,
    }

    # Если запрос от HTMX, возвращаем только блок товаров
    if request.headers.get('HX-Request'):
        return render(request, 'shop/partials/_product_grid.html', context)

    return render(request, 'shop/home.html', context)

# Функция для списка товаров
def product_list(request):
    category_slug = request.GET.get('category')

    # Фильтруем товары
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, available=True)
        selected_category = Category.objects.get(slug=category_slug)
    else:
        products = Product.objects.filter(available=True)
        selected_category = None

    categories = Category.objects.all()

    # Если запрос от HTMX, возвращаем только partial
    if request.headers.get('HX-Request'):
        return render(request, 'shop/partials/_product_grid.html', {
            'products': products
        })

    # Обычный запрос - полная страница
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'featured_products': products[:8]  # или ваша логика featured
    })


# Функция для деталей товара
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    # Похожие товары из той же категории
    related_products = Product.objects.filter(
        category=product.category,
        in_stock=True
    ).exclude(id=product.id)[:8]  # 8 товаров максимум

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


# Функция для товаров категории
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category,
        in_stock=True
    ).select_related('category')
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/home.html', context)


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(in_stock=True)
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(sku__icontains=query)
        )
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'shop/product_search.html', context)