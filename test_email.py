#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spradar_api.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=== Brevo SMTP Ayarları ===")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"TLS: {settings.EMAIL_USE_TLS}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
print(f"Timeout: {getattr(settings, 'EMAIL_TIMEOUT', 'Not set')}")
print("\n" + "="*50)
print("Test email gönderiliyor...\n")

try:
    result = send_mail(
        subject='FX Futbol - Email Doğrulama Test',
        message='Bu bir test emailidir. Eğer bu emaili aldıysanız, email doğrulama sistemi çalışıyor demektir! 🎉',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['destek@fxfutbol.community'],
        fail_silently=False,
    )
    print(f"✅ BAŞARILI! Email gönderildi.")
    print(f"Gönderilen email sayısı: {result}")
    print("\nLütfen destek@fxfutbol.community adresini kontrol edin.")
except Exception as e:
    print(f"❌ HATA: {e}")
    import traceback
    traceback.print_exc()
