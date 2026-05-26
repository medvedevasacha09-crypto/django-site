from django.contrib import admin
from .models import (
    Category, Brand, Product, SaleProduct,
    NewsletterSubscriber, Rating, Order, OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'in_stock', 'is_hit', 'created_at', 'updated_at')
    list_filter = ('category', 'brand', 'is_hit', 'in_stock', 'created_at')
    search_fields = ('name',)
    list_editable = ('in_stock', 'is_hit', 'price')


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'sale_price', 'active', 'created_at', 'updated_at')
    list_filter = ('active',)
    list_editable = ('active',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at')
    search_fields = ('email', 'name')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'score', 'created_at')
    list_filter = ('score',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'delivery_type', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'delivery_type', 'created_at')
    search_fields = ('full_name', 'phone', 'email')
    list_editable = ('status',)
    inlines = [OrderItemInline]