from .settings import *

# Production ayarları
DEBUG = False

ALLOWED_HOSTS = ['fxfutbol.com.tr', 'www.fxfutbol.com.tr', '167.71.74.229', 'localhost']

CSRF_TRUSTED_ORIGINS = [
    'https://fxfutbol.com.tr',
    'https://www.fxfutbol.com.tr',
]

# Static files
STATIC_ROOT = '/var/www/spradar/staticfiles/'
STATIC_URL = '/static/'

# Security settings
SECURE_SSL_REDIRECT = False  # Nginx halledecek
SESSION_COOKIE_SECURE = False  # Nginx halledecek
CSRF_COOKIE_SECURE = False  # Nginx halledecek

# CORS (API için)
CORS_ALLOWED_ORIGINS = [
    'https://fxfutbol.com.tr',
    'http://fxfutbol.com.tr',
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/www/spradar/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Together AI API Key
TOGETHER_API_KEY = "07e297e19eaabe78c4ae52006f8d7ea67d6470727fff514aba20559fb273ea31"
