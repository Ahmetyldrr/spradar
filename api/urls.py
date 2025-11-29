"""
🎯 API URL Routing - Web Pages + REST API
"""

from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from .views import (
    # Web Views
    match_list_view,
    match_list_table_view,  # YENİ: Table view with pagination
    match_detail_view,
    match_detail_api,  # AJAX için
    match_detail_friendly_url,  # SEO-friendly URL
    comeback_list_view,
    comeback_detail_view,
    # API ViewSets
    LeagueComebackSummaryViewSet,
    DailyMatchCommentaryViewSet,
    ComprehensiveComebackAnalysisViewSet,
    # AI Chat API
    match_chat_api,
    match_chat_history_api,
    match_chat_clear_api,
    match_list_api  # YENİ: AJAX match list API
)
from .auth_views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    history_view,
    credit_history_view,
    purchase_credits_view,
    payment_info_view,
    buy_credits_view,
    supervisor_list_view,
    supervisor_purchase_view,
    supervisor_payment_info_view,
    supervisor_panel_view,
    supervisor_approve_order_view,
    supervisor_reject_order_view,
    supervisor_settings_view,
    supervisor_application_view,
    supervisor_application_status_view,
    credit_transfer_view,
    # Yeni sayfalar
    about_view,
    help_view,
    submit_support_ticket,
    announcements_view,
    mark_announcement_read,
)

# Router oluştur (API için)
router = DefaultRouter()
router.register(r'leagues', LeagueComebackSummaryViewSet, basename='league')
router.register(r'daily', DailyMatchCommentaryViewSet, basename='daily')
router.register(r'comebacks', ComprehensiveComebackAnalysisViewSet, basename='comeback')

urlpatterns = [
    # Web Pages
    path('', match_list_table_view, name='match_list'),  # Ana sayfa - ESKİ tablo
    path('professional/', lambda request: render(request, 'match_list_professional.html'), name='match_list_professional'),  # YENİ: Profesyonel görünüm
    path('matches/', match_list_table_view, name='match_list_table'),  # Table view
    path('sidebar/', match_list_view, name='match_list_sidebar'),  # Sidebar view (yedek)
    
    # SEO-Friendly URL: /matches/turkey/super-lig/fenerbahce/galatasaray/
    path('matches/<slug:country_slug>/<slug:league_slug>/<slug:home_slug>/<slug:away_slug>/', 
         match_detail_friendly_url, name='match_detail_friendly'),
    
    path('api/matches/<int:match_id>/', match_detail_api, name='match_detail_api'),  # AJAX için
    path('comebacks/', comeback_list_view, name='comeback_list'),
    path('comebacks/<int:match_id>/', comeback_detail_view, name='comeback_detail'),
    
    # AI Chat API
    path('api/chat/<int:match_id>/', match_chat_api, name='match_chat'),
    path('api/chat/<int:match_id>/history/', match_chat_history_api, name='match_chat_history'),
    path('api/chat/<int:match_id>/clear/', match_chat_clear_api, name='match_chat_clear'),
    
    # Match List API (YENİ: AJAX için)
    path('api/matches/', match_list_api, name='match_list_api'),
    
    # Authentication URLs
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/history/', history_view, name='history'),
    path('accounts/credits/', credit_history_view, name='credit_history'),
    
    # Kredi Satın Alma
    path('accounts/buy-credits/', buy_credits_view, name='buy_credits'),
    path('accounts/purchase/', purchase_credits_view, name='purchase_credits'),
    path('accounts/payment/<int:purchase_id>/', payment_info_view, name='payment_info'),
    
    # Kredi Transfer
    path('accounts/transfer/', credit_transfer_view, name='credit_transfer'),
    
    # Bilgi Sayfaları
    path('about/', about_view, name='about'),
    path('help/', help_view, name='help'),
    path('help/submit/', submit_support_ticket, name='submit_support_ticket'),
    path('announcements/', announcements_view, name='announcements'),
    path('announcements/<int:announcement_id>/read/', mark_announcement_read, name='mark_announcement_read'),
    
    # P2P Supervisor (Satıcı) URLs
    path('supervisors/', supervisor_list_view, name='supervisor_list'),
    path('supervisors/<int:supervisor_id>/purchase/', supervisor_purchase_view, name='supervisor_purchase'),
    path('supervisors/payment/<int:purchase_id>/', supervisor_payment_info_view, name='supervisor_payment_info'),
    path('supervisor/panel/', supervisor_panel_view, name='supervisor_panel'),
    path('supervisor/approve/<int:purchase_id>/', supervisor_approve_order_view, name='supervisor_approve_order'),
    path('supervisor/reject/<int:purchase_id>/', supervisor_reject_order_view, name='supervisor_reject_order'),
    path('supervisor/settings/', supervisor_settings_view, name='supervisor_settings'),
    path('supervisor/apply/', supervisor_application_view, name='supervisor_application'),
    path('supervisor/application-status/', supervisor_application_status_view, name='supervisor_application_status'),
    
    # REST API
    path('api/', include(router.urls)),
]
