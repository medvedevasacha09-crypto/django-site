from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),

    path('about/', views.about, name='about'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Сторінка парфумів (вибери одну назву функції з views.py)
    path('parfume/', views.parfume, name='parfume'),

    path('cosmetics/', views.cosmetics, name='cosmetics'),
    path('clothing/', views.clothing, name='clothing'),
    path('footwear/', views.footwear, name='footwear'),
    path('bag/', views.bag, name='bag'),
]

# Ось тут була помилка — треба додати "+ static..." до списку urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
