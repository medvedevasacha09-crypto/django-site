from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NewsletterSubscriber, Rating, Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=50, required=False, label="Ім'я")
    last_name = forms.CharField(max_length=50, required=False, label='Прізвище')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewsletterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Ім'я",
                           widget=forms.TextInput(attrs={'placeholder': "Ваше ім'я"}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'}))


class RatingForm(forms.Form):
    SCORE_CHOICES = [(i, f'{i} ★') for i in range(1, 6)]
    score = forms.ChoiceField(choices=SCORE_CHOICES, label='Оцінка', widget=forms.RadioSelect)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'email', 'delivery_type', 'city', 'branch_number')
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Прізвище Ім\'я По батькові'}),
            'phone': forms.TextInput(attrs={'placeholder': '+380XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'city': forms.TextInput(attrs={'placeholder': 'Місто'}),
            'branch_number': forms.TextInput(attrs={'placeholder': 'Номер відділення'}),
        }
        labels = {
            'full_name': 'ПІБ',
            'phone': 'Телефон',
            'email': 'Email',
            'delivery_type': 'Спосіб доставки',
            'city': 'Місто',
            'branch_number': 'Номер відділення',
        }


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'}))


class PasswordResetConfirmForm(forms.Form):
    code = forms.CharField(max_length=6, label='Код з email',
                           widget=forms.TextInput(attrs={'placeholder': '6-значний код'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Новий пароль'}),
                                   label='Новий пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль'}),
                                    label='Підтвердження пароля')

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Паролі не співпадають.')
        return cleaned