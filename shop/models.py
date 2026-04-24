from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категорія")
    # Тепер фото не обов'язкове при створенні
    image = models.ImageField(
        upload_to='categories/',
        verbose_name="Зображення",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name="Бренд")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    # Тут теж робимо фото необов'язковим для старту
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Фото",
        null=True,
        blank=True
    )
    is_hit = models.BooleanField(default=False, verbose_name="Хіт продажів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        brand_name = self.brand.name if self.brand else "Без бренду"
        return f"{brand_name} - {self.name}"