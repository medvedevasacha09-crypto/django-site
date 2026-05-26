from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),

    # Товар
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Категорії (універсальна + окремі)
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('parfume/', views.parfume, name='parfume'),
    path('cosmetics/', views.cosmetics, name='cosmetics'),
    path('clothing/', views.clothing, name='clothing'),
    path('footwear/', views.footwear, name='footwear'),
    path('bag/', views.bag, name='bag'),

    # Кошик (лаба 7)
    path('cart/', views.bag_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),

    # Розсилка
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # Авторизація (лаба 8)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('delivery/', views.delivery, name='delivery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)