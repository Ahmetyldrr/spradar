"""
🎯 Django REST Framework Views - API Endpoints + Web Pages
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json

from .models import (
    LeagueComebackSummary, 
    DailyMatchCommentary, 
    ComprehensiveComebackAnalysis, 
    MatchChatHistory,
    CommentHistory
)
from .serializers import (
    LeagueComebackSummarySerializer,
    DailyMatchCommentarySerializer,
    ComprehensiveComebackAnalysisSerializer,
    MatchChatHistorySerializer,
    ChatRequestSerializer
)
from .ai_helper import ai_chat


# ==============================================================================
# WEB PAGES (Template Views)
# ==============================================================================

def match_list_table_view(request):
    """Maç listesi - Profesyonel tablo görünümü (Show More ile)"""
    
    # Tarih filtresi
    selected_date = request.GET.get('date')
    
    if not selected_date:
        # Tarih seçilmediyse TÜM maçları göster (son 7 gün)
        from datetime import datetime, timedelta
        
        # Son 7 günün maçlarını al
        today = datetime.now()
        date_list = [(today - timedelta(days=i)).strftime('%d/%m/%y') for i in range(-3, 4)]  # 3 gün önce, bugün, 3 gün sonra
        
        matches = DailyMatchCommentary.objects.filter(match_date__in=date_list).order_by('match_date', 'match_time')
        display_date = ''  # Boş = tüm tarihler
    else:
        # HTML date input'tan gelen YYYY-MM-DD formatını DD/MM/YY'ye çevir
        try:
            from datetime import datetime
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d/%m/%y')
            matches = DailyMatchCommentary.objects.filter(match_date=formatted_date).order_by('match_time')
            display_date = selected_date
        except:
            from datetime import datetime, timedelta
            today = datetime.now()
            date_list = [(today - timedelta(days=i)).strftime('%d/%m/%y') for i in range(-3, 4)]
            matches = DailyMatchCommentary.objects.filter(match_date__in=date_list).order_by('match_date', 'match_time')
            display_date = ''
    
    # Ülke filtresi
    selected_country = request.GET.get('country', '')
    if selected_country:
        matches = matches.filter(country=selected_country)
    
    # Lig filtresi (ülke seçiliyse sadece o ülkenin ligleri)
    selected_league = request.GET.get('league', '')
    if selected_league:
        matches = matches.filter(league=selected_league)
    
    # Saat aralığı filtresi
    time_from = request.GET.get('time_from', '')
    time_to = request.GET.get('time_to', '')
    
    if time_from:
        matches = matches.filter(match_time__gte=time_from)
    
    if time_to:
        matches = matches.filter(match_time__lte=time_to)
    
    # Takım arama
    search_query = request.GET.get('search', '')
    if search_query:
        matches = matches.filter(
            Q(home_team_name__icontains=search_query) |
            Q(away_team_name__icontains=search_query)
        )
    
    # Filtre seçenekleri için veriler - TÜM maçlardan al
    if selected_date and display_date:
        # Belirli tarih seçiliyse sadece o tarih
        from datetime import datetime
        date_obj = datetime.strptime(display_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d/%m/%y')
        all_matches_for_filters = DailyMatchCommentary.objects.filter(match_date=formatted_date)
    else:
        # Tarih seçili değilse TÜM maçlar
        all_matches_for_filters = DailyMatchCommentary.objects.all()
    
    # TÜM ülkeler
    all_countries = all_matches_for_filters.values_list('country', flat=True).distinct().order_by('country')
    
    # Eğer ülke seçiliyse, sadece o ülkenin liglerini göster
    if selected_country:
        available_leagues = all_matches_for_filters.filter(country=selected_country).values_list('league', flat=True).distinct().order_by('league')
    else:
        available_leagues = all_matches_for_filters.values_list('league', flat=True).distinct().order_by('league')
    
    # İstatistikler
    countries_count = all_matches_for_filters.values('country').distinct().count()
    leagues_count = all_matches_for_filters.values('league').distinct().count()
    
    # TÜM maçları gönder (pagination YOK - Show More JS ile yapılacak)
    context = {
        'matches': matches,  # QuerySet olarak tüm maçlar
        'selected_date': display_date,
        'selected_country': selected_country,
        'selected_league': selected_league,
        'time_from': time_from,
        'time_to': time_to,
        'search_query': search_query,
        'countries': all_countries,
        'leagues': available_leagues,  # Dinamik lig listesi
        'countries_count': countries_count,
        'leagues_count': leagues_count,
    }
    
    return render(request, 'match_list_table.html', context)


def match_list_view(request):
    """Günlük maçları Ülke > Lig hiyerarşisinde listele (ESKİ SIDEBAR VERSION)"""
    selected_date = request.GET.get('date')
    
    if not selected_date:
        # Bugünün tarihi (DD/MM/YY formatında)
        from datetime import datetime
        selected_date = datetime.now().strftime('%d/%m/%y')
    else:
        # HTML date input'tan gelen YYYY-MM-DD formatını DD/MM/YY'ye çevir
        try:
            from datetime import datetime
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            selected_date = date_obj.strftime('%d/%m/%y')
        except:
            selected_date = datetime.now().strftime('%d/%m/%y')
    
    # Veritabanında DD/MM/YY formatında arama yap
    matches = DailyMatchCommentary.objects.filter(match_date=selected_date).order_by('match_time')
    
    # Tüm maçlar (saate göre sıralı)
    all_matches = list(matches)
    
    # Ülke > Lig > Maçlar şeklinde grupla
    grouped_matches = {}
    for match in matches:
        country = match.country or 'Diğer'
        league = match.league or 'Genel'
        
        if country not in grouped_matches:
            grouped_matches[country] = {}
        
        if league not in grouped_matches[country]:
            grouped_matches[country][league] = []
        
        grouped_matches[country][league].append(match)
    
    # Son 30 günde maç olan tarihleri bul
    from datetime import datetime, timedelta
    from django.db.models import Count
    
    available_dates = []
    today = datetime.now()
    
    for i in range(30):
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime('%d/%m/%y')
        
        count = DailyMatchCommentary.objects.filter(match_date=date_str).count()
        
        if count > 0:
            available_dates.append({
                'date': check_date.strftime('%Y-%m-%d'),  # HTML input için
                'display': check_date.strftime('%d %B %Y'),  # Görüntüleme için
                'count': count
            })
    
    # Display için YYYY-MM-DD formatına geri çevir (HTML date input için)
    display_date = selected_date
    try:
        from datetime import datetime
        date_obj = datetime.strptime(selected_date, '%d/%m/%y')
        display_date = date_obj.strftime('%Y-%m-%d')
    except:
        pass
    
    context = {
        'all_matches': all_matches,  # Tüm maçlar (saate göre)
        'grouped_matches': grouped_matches,  # Ülke/Lig grubu
        'available_dates': available_dates,  # Son 30 günün tarihleri
        'selected_date': display_date,  # HTML input için YYYY-MM-DD
        'selected_date_display': selected_date  # Gösterim için DD/MM/YY
    }
    
    return render(request, 'match_sidebar.html', context)


def match_detail_api(request, match_id):
    """AJAX için maç detayı JSON olarak döndür"""
    from django.http import JsonResponse
    
    match = get_object_or_404(DailyMatchCommentary, match_id=match_id)
    
    # JSON yorumu parse et
    commentary = match.commentary_json
    if isinstance(commentary, str):
        commentary = json.loads(commentary)
    
    return JsonResponse({
        'match_id': match.match_id,
        'match_date': str(match.match_date),
        'match_time': match.match_time,
        'country': match.country,
        'league': match.league,
        'home_team_name': match.home_team_name,
        'away_team_name': match.away_team_name,
        'commentary_json': commentary
    })


def match_detail_friendly_url(request, country_slug, league_slug, home_slug, away_slug):
    """
    SEO-Friendly URL: /matches/turkey/super-lig/fenerbahce/galatasaray/
    """
    from django.utils.text import slugify
    
    # Slug'lardan orijinal isimleri bul (en yakın eşleşme)
    matches = DailyMatchCommentary.objects.all()
    
    for match in matches:
        # Slugify ile karşılaştır
        if (slugify(match.country or '') == country_slug and
            slugify(match.league or '') == league_slug and
            slugify(match.home_team_name) == home_slug and
            slugify(match.away_team_name) == away_slug):
            
            # JSON yorumu parse et
            commentary = match.commentary_json
            if isinstance(commentary, str):
                commentary = json.loads(commentary)
            
            context = {
                'match': match,
                'commentary': commentary
            }
            
            return render(request, 'match_detail.html', context)
    
    # Bulunamadı
    from django.http import Http404
    raise Http404("Maç bulunamadı")


def match_detail_view(request, match_id):
    """Maç detay sayfası - Yorumları göster"""
    match = get_object_or_404(DailyMatchCommentary, match_id=match_id)
    
    # JSON yorumu parse et
    commentary = match.commentary_json
    if isinstance(commentary, str):
        commentary = json.loads(commentary)
    
    context = {
        'match': match,
        'commentary': commentary
    }
    
    return render(request, 'match_detail.html', context)


def comeback_list_view(request):
    """Comeback analizlerini listele"""
    matches = ComprehensiveComebackAnalysis.objects.all().order_by('-combined_comeback_score')[:50]
    
    context = {
        'matches': matches
    }
    
    return render(request, 'comeback_list.html', context)


def comeback_detail_view(request, match_id):
    """Comeback analizi detay sayfası"""
    match = get_object_or_404(ComprehensiveComebackAnalysis, match_id=match_id)
    
    # JSON yorumu parse et
    commentary = match.commentary_json
    if isinstance(commentary, str):
        commentary = json.loads(commentary)
    
    context = {
        'match': match,
        'commentary': commentary
    }
    
    return render(request, 'match_detail.html', context)


# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================


class LeagueComebackSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    League Comeback Summary API
    
    Endpoints:
    - GET /api/leagues/                    # Tüm sezonları listele
    - GET /api/leagues/{season_id}/        # Belirli sezon detayı
    - GET /api/leagues/?league_name=...    # Liga göre filtrele
    - GET /api/leagues/?min_matches=10     # En az maç sayısı
    """
    queryset = LeagueComebackSummary.objects.all()
    serializer_class = LeagueComebackSummarySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['league_name', 'season_name']
    ordering_fields = ['match_count', 'season_id']
    ordering = ['-match_count']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Liga göre filtrele
        league_name = self.request.query_params.get('league_name', None)
        if league_name:
            queryset = queryset.filter(league_name__icontains=league_name)
        
        # Min maç sayısı
        min_matches = self.request.query_params.get('min_matches', None)
        if min_matches:
            queryset = queryset.filter(match_count__gte=int(min_matches))
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Genel istatistikler
        GET /api/leagues/stats/
        """
        total_seasons = self.get_queryset().count()
        total_matches = sum([s.match_count for s in self.get_queryset() if s.match_count])
        
        return Response({
            'total_seasons': total_seasons,
            'total_matches': total_matches,
            'avg_matches_per_season': total_matches / total_seasons if total_seasons > 0 else 0
        })


class DailyMatchCommentaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Daily Match Commentary API
    
    Endpoints:
    - GET /api/daily/                      # Tüm günlük maçlar
    - GET /api/daily/{match_id}/           # Belirli maç detayı
    - GET /api/daily/?date=2025-11-05      # Tarihe göre filtrele
    - GET /api/daily/?league=...           # Liga göre filtrele
    - GET /api/daily/?team=...             # Takıma göre filtrele
    """
    queryset = DailyMatchCommentary.objects.all()
    serializer_class = DailyMatchCommentarySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['home_team_name', 'away_team_name', 'league', 'country']
    ordering_fields = ['match_date', 'match_time']
    ordering = ['-match_date', 'match_time']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Tarihe göre filtrele
        date = self.request.query_params.get('date', None)
        if date:
            queryset = queryset.filter(match_date=date)
        
        # Liga göre filtrele
        league = self.request.query_params.get('league', None)
        if league:
            queryset = queryset.filter(league__icontains=league)
        
        # Takıma göre filtrele
        team = self.request.query_params.get('team', None)
        if team:
            queryset = queryset.filter(
                Q(home_team_name__icontains=team) | Q(away_team_name__icontains=team)
            )
        
        return queryset


class ComprehensiveComebackAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Comprehensive Comeback Analysis API
    
    Endpoints:
    - GET /api/comebacks/                          # Tüm comeback analizleri
    - GET /api/comebacks/{match_id}/               # Belirli maç
    - GET /api/comebacks/?min_score=10             # Min comeback skoru
    - GET /api/comebacks/?data_quality=OK          # Sadece kaliteli veriler
    - GET /api/comebacks/?team=...                 # Takıma göre
    - GET /api/comebacks/top/                      # En yüksek skorlu maçlar
    """
    queryset = ComprehensiveComebackAnalysis.objects.all()
    serializer_class = ComprehensiveComebackAnalysisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['home_team_name', 'away_team_name']
    ordering_fields = ['combined_comeback_score', 'match_date']
    ordering = ['-combined_comeback_score']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Min comeback skoru
        min_score = self.request.query_params.get('min_score', None)
        if min_score:
            queryset = queryset.filter(combined_comeback_score__gte=float(min_score))
        
        # Data quality filtresi
        quality = self.request.query_params.get('data_quality', None)
        if quality:
            queryset = queryset.filter(data_quality=quality)
        
        # Takıma göre filtrele
        team = self.request.query_params.get('team', None)
        if team:
            queryset = queryset.filter(
                Q(home_team_name__icontains=team) | Q(away_team_name__icontains=team)
            )
        
        # Sezona göre
        season = self.request.query_params.get('season_id', None)
        if season:
            queryset = queryset.filter(season_id=int(season))
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """
        En yüksek skorlu 20 maç
        GET /api/comebacks/top/
        """
        limit = int(request.query_params.get('limit', 20))
        top_matches = self.get_queryset().order_by('-combined_comeback_score')[:limit]
        serializer = self.get_serializer(top_matches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Genel istatistikler
        GET /api/comebacks/stats/
        """
        queryset = self.get_queryset()
        total = queryset.count()
        ok_quality = queryset.filter(data_quality='OK').count()
        
        return Response({
            'total_matches': total,
            'ok_quality': ok_quality,
            'incomplete': total - ok_quality,
            'ok_percentage': (ok_quality / total * 100) if total > 0 else 0
        })


# ==============================================================================
# AI CHAT API ENDPOINTS
# ==============================================================================

@api_view(['POST'])
def match_chat_api(request, match_id):
    """
    Maç için AI ile sohbet et - Üyelik ve Kredi Kontrolü ile
    
    POST /api/chat/{match_id}/
    Body: {"message": "Bu maç hakkında ne düşünüyorsun?"}
    
    NOT: Rate limiting şimdilik kapalı (Redis kurulunca aktif edilecek)
    Kredi sistemi zaten doğal bir rate limiter görevi görüyor.
    """
    
    # 1️⃣ AUTHENTICATION CHECK - Üye değilse reddediyoruz
    if not request.user.is_authenticated:
        return Response({
            'error': 'authentication_required',
            'message': 'Bu özelliği kullanmak için üye olmanız gerekiyor. Kayıt olun ve 10 bedava kredi kazanın!',
            'register_url': '/accounts/register/',
            'login_url': '/accounts/login/',
            'show_membership_modal': True  # Frontend'de modal açmak için
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 2️⃣ CREDIT CHECK - Kredi var mı kontrol et
    user_profile = request.user.profile
    if not user_profile.has_credits(1):
        return Response({
            'error': 'insufficient_credits',
            'message': f'Krediniz yetersiz. Mevcut kredi: {user_profile.credits}. Lütfen kredi paketlerinden satın alın.',
            'current_credits': user_profile.credits,
            'membership_type': user_profile.membership_type,
            'profile_url': '/accounts/profile/',
            'show_upgrade_modal': True  # Frontend'de upgrade modal açmak için
        }, status=status.HTTP_403_FORBIDDEN)
    
    # 3️⃣ MATCH VALIDATION - Maçı bul
    try:
        match = DailyMatchCommentary.objects.get(match_id=match_id)
    except DailyMatchCommentary.DoesNotExist:
        return Response(
            {'error': f'Maç bulunamadı: {match_id}'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 4️⃣ REQUEST VALIDATION
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_message = serializer.validated_data['message']
    
    # 5️⃣ AI PROCESSING - Önceki chat geçmişini al (son 5 mesaj) - SADECE BU KULLANICININ
    previous_chats = MatchChatHistory.objects.filter(
        match_id=match_id,
        user=request.user
    ).order_by('-created_at')[:5]
    chat_history = []
    for chat in reversed(previous_chats):
        chat_history.append({'role': 'user', 'content': chat.user_message})
        chat_history.append({'role': 'assistant', 'content': chat.ai_response})
    
    # Maç context'i hazırla
    match_context = ai_chat.get_match_context(match)
    
    # AI'dan yanıt al
    try:
        ai_response = ai_chat.chat(user_message, match_context, chat_history)
    except Exception as e:
        # AI hatası durumunda kullanıcıya bilgi ver ama kredi düşme
        return Response({
            'error': 'ai_error',
            'message': f'AI şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin. Kredi düşülmedi.',
            'details': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # 6️⃣ CREDIT DEDUCTION - Başarılıysa krediyi düş
    deduct_success = user_profile.deduct_credits(
        amount=1,
        reason=f'AI yorum: {match.home_team_name} vs {match.away_team_name}'
    )
    
    if not deduct_success:
        return Response({
            'error': 'credit_deduction_failed',
            'message': 'Kredi düşülemedi. Lütfen tekrar deneyin veya destek ile iletişime geçin.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 7️⃣ HISTORY SAVE - Chat geçmişine kaydet (KULLANICIYA ÖZEL)
    chat_entry = MatchChatHistory.objects.create(
        match_id=match_id,
        user=request.user,
        user_message=user_message,
        ai_response=ai_response
    )
    
    # 8️⃣ USER COMMENT HISTORY - Kullanıcı yorumunu kaydet
    CommentHistory.objects.create(
        user=request.user,
        match_id=match_id,
        match_info=f'{match.home_team_name} vs {match.away_team_name} | {match.league}',
        user_question=user_message,
        ai_response=ai_response,
        credits_used=1
    )
    
    # 9️⃣ SUCCESS RESPONSE
    return Response({
        'success': True,
        'match_id': match_id,
        'user_message': user_message,
        'ai_response': ai_response,
        'timestamp': chat_entry.created_at,
        'credits': {
            'remaining': user_profile.credits,
            'used': 1,
            'membership_type': user_profile.membership_type
        },
        'match_info': {
            'home_team': match.home_team_name,
            'away_team': match.away_team_name,
            'league': match.league,
            'date': match.match_date,
            'time': match.match_time
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def match_chat_history_api(request, match_id):
    """
    Maç için chat geçmişini getir - SADECE KULLANICININ KENDİ MESAJLARI
    
    GET /api/chat/{match_id}/history/
    
    NOT: Her kullanıcı sadece kendi sohbet geçmişini görür.
    Giriş yapmamış kullanıcılar boş geçmiş görür.
    """
    # Giriş yapmış kullanıcı için filtreleme
    if request.user.is_authenticated:
        chats = MatchChatHistory.objects.filter(
            match_id=match_id,
            user=request.user
        ).order_by('created_at')
    else:
        # Giriş yapmamış kullanıcılar hiçbir mesaj görmesin
        chats = MatchChatHistory.objects.none()
    
    serializer = MatchChatHistorySerializer(chats, many=True)
    
    return Response({
        'match_id': match_id,
        'total_messages': chats.count(),
        'messages': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def match_chat_clear_api(request, match_id):
    """
    Maç için chat geçmişini temizle - SADECE KULLANICININ KENDİ MESAJLARI
    
    DELETE /api/chat/{match_id}/clear/
    """
    # Giriş yapmış kullanıcı kontrolü
    if not request.user.is_authenticated:
        return Response({
            'error': 'authentication_required',
            'message': 'Mesajları silmek için giriş yapmalısınız.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    deleted_count = MatchChatHistory.objects.filter(
        match_id=match_id,
        user=request.user
    ).delete()[0]
    
    return Response({
        'match_id': match_id,
        'deleted_messages': deleted_count,
        'message': 'Chat geçmişiniz temizlendi'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def match_list_api(request):
    """
    Profesyonel tablo için maç listesi API
    
    GET /api/matches/
    Query Params:
        - date: YYYY-MM-DD
        - country: Ülke adı
        - league: Lig adı
        - time_from: HH:MM
        - time_to: HH:MM
    """
    from datetime import datetime
    from django.db.models import Count
    
    # Tarih filtresi
    selected_date = request.GET.get('date')
    
    if not selected_date:
        selected_date = datetime.now().strftime('%d/%m/%y')
    else:
        try:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            selected_date = date_obj.strftime('%d/%m/%y')
        except:
            selected_date = datetime.now().strftime('%d/%m/%y')
    
    # Maçları çek
    matches = DailyMatchCommentary.objects.filter(match_date=selected_date)
    
    # Filtreler
    country = request.GET.get('country', '')
    league = request.GET.get('league', '')
    time_from = request.GET.get('time_from', '')
    time_to = request.GET.get('time_to', '')
    
    if country:
        matches = matches.filter(country=country)
    
    if league:
        matches = matches.filter(league=league)
    
    if time_from:
        matches = matches.filter(match_time__gte=time_from)
    
    if time_to:
        matches = matches.filter(match_time__lte=time_to)
    
    # Her maç için chat sayısını ve AI tahmini ekle
    matches_data = []
    for match in matches.order_by('match_time'):
        # Chat sayısı
        chat_count = MatchChatHistory.objects.filter(match_id=match.match_id).count()
        
        # AI tahmini (son chat'ten çıkar)
        ai_prediction = '-'
        last_chat = MatchChatHistory.objects.filter(match_id=match.match_id).order_by('-created_at').first()
        if last_chat:
            # AI response'dan skor çıkarmaya çalış (regex ile)
            import re
            response = last_chat.ai_response
            # "2-1", "1-0" gibi skorları ara
            score_pattern = r'\b(\d{1})-(\d{1})\b'
            scores = re.findall(score_pattern, response)
            if scores:
                ai_prediction = f"{scores[0][0]}-{scores[0][1]}"
        
        matches_data.append({
            'match_id': match.match_id,
            'match_date': match.match_date,
            'match_time': match.match_time,
            'country_name': match.country,
            'tournament_name': match.league,
            'home_team_name': match.home_team_name,
            'away_team_name': match.away_team_name,
            'home_team_id': match.home_team_id,
            'away_team_id': match.away_team_id,
            'chat_count': chat_count,
            'ai_prediction': ai_prediction,
        })
    
    return Response({
        'date': selected_date,
        'total_matches': len(matches_data),
        'matches': matches_data
    }, status=status.HTTP_200_OK)
