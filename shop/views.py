from django.shortcuts import render


def home(request):
    # Контекст з даними про ваш магазин
    context = {
        'title': 'Beauty Shop — Магазин косметики',
        'categories': ['Догляд за обличчям', 'Парфуми', 'Макіяж'],
        'welcome_message': 'Вітаємо у нашому магазині найкращої косметики!'
    }
    return render(request, 'shop/index.html', context)


def about(request):
    context = {
        'title': 'Про наш магазин',
        'description': 'Ми продаємо лише органічну косметику з 2024 року.'
    }
    return render(request, 'shop/about.html', context)


from django.shortcuts import render

# Create your views here.
