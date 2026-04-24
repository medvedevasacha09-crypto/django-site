from django.contrib import admin
from .models import Category, Product, Brand

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Відображаємо назву, ціну та дати (як у завданні)
    list_display = ('name', 'price', 'is_hit', 'created_at', 'updated_at')
    # Додаємо фільтрацію по датах та категоріях
    list_filter = ('category', 'is_hit', 'created_at')
    # Пошук за назвою
    search_fields = ('name',)

admin.site.register(Category)
admin.site.register(Brand)