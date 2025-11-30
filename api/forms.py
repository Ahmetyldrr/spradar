"""
Django Forms - Kullanıcı Kaydı ve Giriş
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Kullanıcı kayıt formu - Bootstrap 5 stillendirilmiş
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'E-posta adresiniz'
        })
    )
    first_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Adınız (opsiyonel)'
        })
    )
    last_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Soyadınız (opsiyonel)'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Bootstrap stilleri ekle
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Kullanıcı adı'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Şifre'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Şifre (tekrar)'
        })
        
        # Yardım metinlerini güncelle
        self.fields['username'].help_text = 'Harf, rakam ve @/./+/-/_ karakterleri kullanabilirsiniz.'
        self.fields['password1'].help_text = 'En az 8 karakter, sadece rakamlardan oluşmamalı.'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
            # Profile otomatik oluşacak (signal sayesinde)
        
        return user


class UserLoginForm(AuthenticationForm):
    """
    Kullanıcı giriş formu - Bootstrap 5 stillendirilmiş
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Kullanıcı adı',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Şifre'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Beni hatırla'
    )
