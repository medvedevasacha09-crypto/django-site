from django.shortcuts import render


def home(request):
    # Контекст з даними про ваш магазин
    context = {
        'title': 'Fluffy prostir',
        'categories': ['Парфуми',  'Косметика','Одяг', 'Взуття', 'Сумки'],
    }
    return render(request, 'shop/index.html', context)


def about(request):
    context = {
        'title': 'Про наш магазин',
        'description': 'Ми продаємо лише органічну косметику з 2024 року.'
    }
    return render(request, 'shop/about.html', context)


from django.shortcuts import render

from django.shortcuts import render

def index(request):
    categories = ['Парфуми',  'Косметика','Одяг', 'Взуття', 'Сумки']

from django.shortcuts import render
def index(request):
    return render(request, 'shop/index.html')

def parfume(request):
    return render(request, 'shop/parfume.html')

def cosmetics(request):
    return render(request, 'shop/cosmetics.html')

def clothing(request):
    return render(request, 'shop/clothing.html')


def footwear(request):
    return render(request, 'shop/footwear.html')

def bag(request):
    return render(request, 'shop/bag.html')