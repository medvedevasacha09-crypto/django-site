from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def index(request):
    categories = Category.objects.all()
    hits = Product.objects.filter(is_hit=True)
    return render(request, 'shop/index.html', {
        'categories': categories,
        'hits': hits
    })

# Нова функція для детальної сторінки товару
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': Category.objects.all()
    })

def parfume(request):
    items = Product.objects.filter(category__name__icontains='Парфуми')
    return render(request, 'shop/parfume.html', {'items': items, 'categories': Category.objects.all()})

def cosmetics(request):
    items = Product.objects.filter(category__name__icontains='косметика')
    return render(request, 'shop/cosmetics.html', {'items': items, 'categories': Category.objects.all()})

def clothing(request):
    items = Product.objects.filter(category__name__icontains='одяг')
    return render(request, 'shop/clothing.html', {'items': items, 'categories': Category.objects.all()})

def footwear(request):
    items = Product.objects.filter(category__name__icontains='взуття')
    return render(request, 'shop/footwear.html', {'items': items, 'categories': Category.objects.all()})

def bag(request):
    items = Product.objects.filter(category__name__icontains='сумк')
    return render(request, 'shop/bag.html', {'items': items, 'categories': Category.objects.all()})

def about(request):
    return render(request, 'shop/about.html', {'categories': Category.objects.all()})

