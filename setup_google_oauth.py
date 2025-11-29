"""
Google OAuth Setup Script
Bu script'i çalıştırarak Google OAuth'u otomatik ayarlayabilirsin
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spradar_api.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Site ayarları
site, created = Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': 'fxfutbol.com.tr',
        'name': 'FX Futbol'
    }
)

if not created:
    site.domain = 'fxfutbol.com.tr'
    site.name = 'FX Futbol'
    site.save()
    print(f"✅ Site güncellendi: {site.domain}")
else:
    print(f"✅ Site oluşturuldu: {site.domain}")

# Google OAuth App ayarları
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

if not google_client_id or not google_client_secret:
    print("❌ HATA: .env dosyasında GOOGLE_CLIENT_ID ve GOOGLE_CLIENT_SECRET bulunamadı!")
    exit(1)

# Google App oluştur veya güncelle
google_app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google',
        'client_id': google_client_id,
        'secret': google_client_secret,
    }
)

if not created:
    google_app.client_id = google_client_id
    google_app.secret = google_client_secret
    google_app.save()
    print(f"✅ Google OAuth App güncellendi")
else:
    print(f"✅ Google OAuth App oluşturuldu")

# Site'a Google App'i ekle
google_app.sites.add(site)
print(f"✅ Google App, {site.domain} site'ına eklendi")

print("\n" + "="*60)
print("🎉 Google OAuth Kurulumu Tamamlandı!")
print("="*60)
print(f"Site: {site.domain}")
print(f"Google Client ID: {google_client_id[:20]}...")
print(f"Redirect URI: https://{site.domain}/accounts/google/login/callback/")
print("="*60)
