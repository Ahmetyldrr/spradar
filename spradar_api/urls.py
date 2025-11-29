"""
URL configuration for spradar_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from django.http import JsonResponse


def api_root(request):
    """API Root - Mevcut endpoints"""
    return JsonResponse({
        'message': 'Spradar Analytics API',
        'version': '1.0.0',
        'endpoints': {
            'leagues': '/api/leagues/',
            'daily_commentaries': '/api/daily/',
            'comeback_analysis': '/api/comebacks/',
            'admin': '/admin/',
            'api_docs': '/api/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # django-allauth URLs
    # Custom redirects for URL compatibility
    path('accounts/register/', RedirectView.as_view(url='/accounts/signup/', permanent=True)),
    path('', include('api.urls')),  # Ana sayfa için
]
