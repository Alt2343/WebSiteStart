from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


from django.db import models


class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Мужской'),
        ('women', 'Женский'),
        ('unisex', 'Унисекс'),
        ('kids', 'Детский'),
    ]
    # Основная информация
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    brand = models.CharField(max_length=100, null=True, blank=True ,verbose_name="Бренд")
    sku = models.CharField(max_length=50, unique=True,verbose_name="Артикул")
    main_image = models.ImageField(upload_to='products/main/%Y/%m/%d/',verbose_name='Главное фото',blank=True,null=True)
    size = models.CharField(max_length=10, verbose_name='Размер', blank=True, null=True)
    color = models.CharField(max_length=10, verbose_name='Цвет', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex', verbose_name="Пол")
    description = models.TextField(blank=True, verbose_name='Описание')
    material = models.CharField(max_length=200, verbose_name="Материал")
    country_of_origin = models.CharField(max_length=100, blank=True, verbose_name="Страна производства")
    # Связь с категорией
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',verbose_name='Категория')
    # Цена и наличие
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Цена')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name