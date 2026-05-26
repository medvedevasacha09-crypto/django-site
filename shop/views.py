from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import random
import string

from .models import Category, Product, SaleProduct, NewsletterSubscriber, Rating, Order, OrderItem
from .forms import RegisterForm, NewsletterForm, RatingForm, OrderForm, PasswordResetRequestForm, \
    PasswordResetConfirmForm


# Допоміжна функція для отримання категорій у кожну в'юшку
def get_base_context():
    return {'all_categories': Category.objects.all()}


def index(request):
    ctx = get_base_context()
    # Отримуємо хіти та акції
    ctx['hits'] = Product.objects.filter(is_hit=True)
    ctx['sales'] = SaleProduct.objects.filter(active=True).select_related('product')
    # Тепер у ctx вже є 'all_categories' завдяки get_base_context()
    return render(request, 'shop/index.html', ctx)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ctx = get_base_context()
    ctx['product'] = product
    ctx['avg_rating'] = product.average_rating()
    ctx['rating_form'] = RatingForm()
    ctx['user_rated'] = (
        Rating.objects.filter(product=product, user=request.user).exists()
        if request.user.is_authenticated else False
    )
    if request.method == 'POST' and 'score' in request.POST:
        if not request.user.is_authenticated:
            messages.warning(request, 'Щоб залишити оцінку — увійдіть в акаунт.')
            return redirect('product_detail', pk=pk)
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                product=product, user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
            messages.success(request, 'Дякуємо за оцінку!')
        return redirect('product_detail', pk=pk)
    return render(request, 'shop/product_detail.html', ctx)


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    ctx = get_base_context()
    ctx['category'] = category
    # Використовуємо 'products', як у вашому шаблоні category_detail.html
    ctx['products'] = Product.objects.filter(category=category)
    return render(request, 'shop/category_detail.html', ctx)


# Функції для швидких фільтрів (меню)
def parfume(request):
    ctx = get_base_context()
    ctx['products'] = Product.objects.filter(category__name__icontains='Парфуми')
    ctx['title'] = 'Парфуми'
    return render(request, 'shop/category_page.html', ctx)


def cosmetics(request):
    ctx = get_base_context()
    ctx['products'] = Product.objects.filter(category__name__icontains='косметика')
    ctx['title'] = 'Косметика'
    return render(request, 'shop/category_page.html', ctx)


def clothing(request):
    ctx = get_base_context()
    ctx['products'] = Product.objects.filter(category__name__icontains='одяг')
    ctx['title'] = 'Одяг'
    return render(request, 'shop/category_page.html', ctx)


def footwear(request):
    ctx = get_base_context()
    ctx['products'] = Product.objects.filter(category__name__icontains='взуття')
    ctx['title'] = 'Взуття'
    return render(request, 'shop/category_page.html', ctx)


def bag(request):
    ctx = get_base_context()
    ctx['products'] = Product.objects.filter(category__name__icontains='сумк')
    ctx['title'] = 'Сумки'
    return render(request, 'shop/category_page.html', ctx)


def about(request):
    return render(request, 'shop/about.html', get_base_context())


def delivery(request):
    return render(request, 'shop/delivery.html', get_base_context())


def bag_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(pid))
            item_total = product.price * qty
            total += item_total
            items.append({'product': product, 'qty': qty, 'total': item_total})
        except Product.DoesNotExist:
            pass

    order_form = OrderForm()
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid() and items:
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = total
            order.save()
            for item in items:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    quantity=item['qty'], price=item['product'].price
                )
            request.session['cart'] = {}
            messages.success(request, f'Замовлення #{order.pk} оформлено! Дякуємо!')
            return redirect('home')

    ctx = get_base_context()
    ctx['cart_items'] = items
    ctx['total'] = total
    ctx['order_form'] = order_form
    return render(request, 'shop/bag.html', ctx)


@require_POST
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'Товар додано до кошика!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def update_cart(request, pk):
    cart = request.session.get('cart', {})
    qty = int(request.POST.get('qty', 1))
    if qty > 0:
        cart[str(pk)] = qty
    else:
        cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        name = form.cleaned_data.get('name', '')
        obj, created = NewsletterSubscriber.objects.get_or_create(
            email=email, defaults={'name': name}
        )
        if created:
            messages.success(request, 'Ви успішно підписались на розсилку!')
        else:
            messages.info(request, 'Цей email вже підписаний.')
    else:
        messages.error(request, 'Введіть коректний email.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Реєстрація успішна!')
        return redirect('home')
    ctx = get_base_context()
    ctx['form'] = form
    return render(request, 'shop/register.html', ctx)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Привіт, {user.username}!')
        return redirect('home')
    ctx = get_base_context()
    ctx['form'] = form
    return render(request, 'shop/login.html', ctx)


def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з акаунту.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.user.is_staff:
        orders = Order.objects.all().prefetch_related('items__product')
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    ctx = get_base_context()
    ctx['orders'] = orders
    return render(request, 'shop/profile.html', ctx)


@login_required
def change_password_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Пароль успішно змінено!')
        return redirect('profile')
    ctx = get_base_context()
    ctx['form'] = form
    return render(request, 'shop/change_password.html', ctx)


def password_reset_request(request):
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            code = ''.join(random.choices(string.digits, k=6))
            request.session['reset_code'] = code
            request.session['reset_user_id'] = user.pk
            send_mail(
                subject='Fluffy — код відновлення пароля',
                message=f'Ваш код: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            messages.success(request, 'Код надіслано на ваш email.')
            return redirect('password_reset_confirm')
        except User.DoesNotExist:
            messages.error(request, 'Користувача з таким email не знайдено.')
    ctx = get_base_context()
    ctx['form'] = form
    return render(request, 'shop/password_reset_request.html', ctx)


def password_reset_confirm(request):
    form = PasswordResetConfirmForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['code']
        new_password = form.cleaned_data['new_password']
        session_code = request.session.get('reset_code')
        user_id = request.session.get('reset_user_id')
        if code == session_code and user_id:
            try:
                user = User.objects.get(pk=user_id)
                user.set_password(new_password)
                user.save()
                del request.session['reset_code']
                del request.session['reset_user_id']
                messages.success(request, 'Пароль змінено! Тепер увійдіть.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Помилка. Спробуйте знову.')
        else:
            messages.error(request, 'Невірний код.')
    ctx = get_base_context()
    ctx['form'] = form
    return render(request, 'shop/password_reset_confirm.html', ctx)