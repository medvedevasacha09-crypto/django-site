from django.shortcuts import render
from .models import Category, Product

# Головна сторінка
def index(request):
    categories = Category.objects.all()
    hits = Product.objects.filter(is_hit=True)
    context = {
        'title': 'Fluffy Prostir - Головна',
        'categories': categories,
        'hits': hits,
    }
    return render(request, 'shop/index.html', context)

# Сторінка "Про нас"
def about(request):
    return render(request, 'shop/about.html', {'categories': Category.objects.all()})

# Категорія: Парфуми
def parfume(request):
    items = Product.objects.filter(category__name__icontains='парфум')
    return render(request, 'shop/parfume.html', {'items': items, 'categories': Category.objects.all()})

# Категорія: Косметика
def cosmetics(request):
    items = Product.objects.filter(category__name__icontains='косметика')
    return render(request, 'shop/cosmetics.html', {'items': items, 'categories': Category.objects.all()})

# Категорія: Одяг
def clothing(request):
    items = Product.objects.filter(category__name__icontains='одяг')
    return render(request, 'shop/clothing.html', {'items': items, 'categories': Category.objects.all()})

# Категорія: Взуття (ЦЕ ВИПРАВИТЬ ТВОЮ ПОМИЛКУ НА СКРИНШОТІ)
def footwear(request):
    items = Product.objects.filter(category__name__icontains='взуття')
    return render(request, 'shop/footwear.html', {'items': items, 'categories': Category.objects.all()})

# Категорія: Сумки
def bag(request):
    items = Product.objects.filter(category__name__icontains='сумки')
    return render(request, 'shop/bag.html', {'items': items, 'categories': Category.objects.all()})