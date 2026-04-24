from django.shortcuts import render
from .models import Category, Product  # Прибрали Review, якщо його немає в models.py # Імпортуємо всі ваші моделі

def index(request):
    # Отримуємо всі товари для головної
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def about(request):
    return render(request, 'shop/about.html')

def parfume(request):
    # Фільтруємо товари, де назва категорії містить "парфум"
    items = Product.objects.filter(category__name__icontains='парфум')
    return render(request, 'shop/parfume.html', {'items': items})

def cosmetics(request):
    # Фільтруємо товари для косметики
    items = Product.objects.filter(category__name__icontains='косметика')
    return render(request, 'shop/cosmetics.html', {'items': items})

def clothing(request):
    items = Product.objects.filter(category__name__icontains='одяг')
    return render(request, 'shop/clothing.html', {'items': items})

def footwear(request):
    items = Product.objects.filter(category__name__icontains='взуття')
    return render(request, 'shop/footwear.html', {'items': items})

def bag(request):
    items = Product.objects.filter(category__name__icontains='сумки')
    return render(request, 'shop/bag.html', {'items': items})