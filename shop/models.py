from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категорія")
    image = models.ImageField(
        upload_to='categories/',
        verbose_name="Зображення",
        null=True,
        blank=True
    )
    # Додаємо ці два поля:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Бренд")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Фото",
        null=True,
        blank=True
    )
    description = models.TextField(verbose_name="Опис", blank=True, default='')
    is_hit = models.BooleanField(default=False, verbose_name="Хіт продажів")
    in_stock = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        brand_name = self.brand.name if self.brand else "Без бренду"
        return f"{brand_name} - {self.name}"

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return None


class SaleProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name='sale')
    discount_percent = models.PositiveIntegerField(verbose_name="Знижка (%)")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Акційна ціна")
    active = models.BooleanField(default=True, verbose_name="Активна акція")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Акційний товар"
        verbose_name_plural = "Акційні товари"

    def __str__(self):
        return f"{self.product.name} — {self.discount_percent}% знижка"


class NewsletterSubscriber(models.Model):
    """Підписка на розсилку — лаба 7"""
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="Ім'я", blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата підписки")

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Підписники"

    def __str__(self):
        return self.email


class Rating(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings', verbose_name="Товар")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач", null=True, blank=True)
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, verbose_name="Оцінка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.product.name} — {self.score}★"


class Order(models.Model):
    """Замовлення — лаба 7+8"""
    DELIVERY_CHOICES = [
        ('nova', 'Нова Пошта'),
        ('ukr', 'Укрпошта'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('confirmed', 'Підтверджено'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Користувач")
    full_name = models.CharField(max_length=200, verbose_name="ПІБ")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES, verbose_name="Доставка")
    city = models.CharField(max_length=100, verbose_name="Місто")
    branch_number = models.CharField(max_length=20, verbose_name="Номер відділення")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сума")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення #{self.pk} — {self.full_name}"


class OrderItem(models.Model):
    """Товари у замовленні"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Замовлення")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    def __str__(self):
        return f"{self.product} x{self.quantity}"

    def get_total(self):
        return self.price * self.quantity