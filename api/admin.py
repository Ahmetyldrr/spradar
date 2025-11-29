from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import (
    LeagueComebackSummary,
    DailyMatchCommentary,
    ComprehensiveComebackAnalysis,
    MatchChatHistory,
    CronService,
    ServiceLog,
    UserProfile,
    CreditTransaction,
    CommentHistory,
    CreditPurchase,
    SupervisorCreditPurchase,
    SupervisorApplication,
    CreditTransfer,
    SupportTicket,
    Announcement,
    UserAnnouncementRead
)


# ==============================================================================
# CRON SERVİSLERİ ADMİN
# ==============================================================================

@admin.register(CronService)
class CronServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name_with_icon',
        'service_type',
        'is_active_badge',
        'cron_schedule',
        'last_run_display',
        'last_status_badge',
        'log_count',
        'success_rate'
    ]
    list_filter = ['service_type', 'is_active', 'last_status']
    search_fields = ['name', 'description']
    readonly_fields = ['last_run', 'last_status', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('name', 'service_type', 'description')
        }),
        ('Zamanlama', {
            'fields': ('cron_schedule', 'is_active')
        }),
        ('Durum', {
            'fields': ('last_run', 'last_status'),
            'classes': ('collapse',)
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def name_with_icon(self, obj):
        """Servis adı ile ikon"""
        icons = {
            'FIXTURE2X': '📊',
            'COMMENTARY': '📝',
            'COMEBACK': '🔥',
            'SRSERVICE': '⚙️',
            'OTHER': '📦',
        }
        icon = icons.get(obj.service_type, '❓')
        return format_html(f'{icon} <strong>{obj.name}</strong>')
    name_with_icon.short_description = 'Servis'
    
    def is_active_badge(self, obj):
        """Aktif durumu badge"""
        if obj.is_active:
            return format_html('<span style="color: green;">✅ Aktif</span>')
        return format_html('<span style="color: red;">❌ Pasif</span>')
    is_active_badge.short_description = 'Durum'
    
    def last_run_display(self, obj):
        """Son çalışma zamanı"""
        if obj.last_run:
            from django.utils import timezone
            diff = timezone.now() - obj.last_run
            hours = diff.total_seconds() / 3600
            
            if hours < 1:
                return format_html(f'<span style="color: green;">{int(diff.total_seconds() / 60)} dk önce</span>')
            elif hours < 24:
                return format_html(f'<span style="color: orange;">{int(hours)} saat önce</span>')
            else:
                return format_html(f'<span style="color: red;">{int(hours / 24)} gün önce</span>')
        return format_html('<span style="color: gray;">Hiç çalışmamış</span>')
    last_run_display.short_description = 'Son Çalışma'
    
    def last_status_badge(self, obj):
        """Son durum badge"""
        if obj.last_status is None:
            return format_html('<span style="color: gray;">-</span>')
        elif obj.last_status:
            return format_html('<span style="color: green;">✅ Başarılı</span>')
        else:
            return format_html('<span style="color: red;">❌ Hatalı</span>')
    last_status_badge.short_description = 'Son Durum'
    
    def log_count(self, obj):
        """Toplam log sayısı"""
        count = obj.logs.count()
        return format_html(f'<a href="/admin/api/servicelog/?service__id__exact={obj.id}">{count} log</a>')
    log_count.short_description = 'Log Sayısı'
    
    def success_rate(self, obj):
        """Başarı oranı"""
        total = obj.logs.count()
        if total == 0:
            return '-'
        success = obj.logs.filter(status='SUCCESS').count()
        rate = (success / total) * 100
        
        color = 'green' if rate >= 80 else 'orange' if rate >= 50 else 'red'
        return format_html('<span style="color: {};">{}</span>', color, f'{rate:.1f}%')
    success_rate.short_description = 'Başarı Oranı'
    
    def get_queryset(self, request):
        """Optimizasyon için log sayısını prefetch et"""
        qs = super().get_queryset(request)
        return qs.annotate(
            log_count_annotate=Count('logs')
        )


# ==============================================================================
# SERVİS LOGLARI ADMİN
# ==============================================================================

@admin.register(ServiceLog)
class ServiceLogAdmin(admin.ModelAdmin):
    list_display = [
        'created_at_display',
        'service_link',
        'operation_name_short',
        'status_badge',
        'duration_display',
        'processed_count',
        'error_count',
    ]
    list_filter = [
        'status',
        'service',
        ('created_at', admin.DateFieldListFilter),
    ]
    search_fields = ['operation_name', 'message', 'service__name']
    readonly_fields = ['created_at', 'service', 'operation_name', 'status', 'message', 'details', 'duration_seconds', 'processed_count', 'error_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('service', 'operation_name', 'status', 'created_at')
        }),
        ('Sonuçlar', {
            'fields': ('duration_seconds', 'processed_count', 'error_count')
        }),
        ('Mesaj ve Detaylar', {
            'fields': ('message', 'details'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Manuel log eklemeyi engelle"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Log değiştirmeyi engelle"""
        return False
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')
    created_at_display.short_description = 'Tarih/Saat'
    created_at_display.admin_order_field = 'created_at'
    
    def service_link(self, obj):
        """Servis linki"""
        return format_html(
            '<a href="/admin/api/cronservice/{}/change/">{}</a>',
            obj.service.id,
            obj.service.name
        )
    service_link.short_description = 'Servis'
    service_link.admin_order_field = 'service'
    
    def operation_name_short(self, obj):
        """Kısa işlem adı"""
        if len(obj.operation_name) > 50:
            return obj.operation_name[:50] + '...'
        return obj.operation_name
    operation_name_short.short_description = 'İşlem'
    
    def status_badge(self, obj):
        """Durum badge"""
        colors = {
            'SUCCESS': 'green',
            'ERROR': 'red',
            'WARNING': 'orange',
            'INFO': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            f'<span style="color: {color};">{obj.status_icon} {obj.get_status_display()}</span>'
        )
    status_badge.short_description = 'Durum'
    status_badge.admin_order_field = 'status'
    
    def duration_display(self, obj):
        """Süre gösterimi"""
        if obj.duration_seconds is None:
            return '-'
        
        if obj.duration_seconds < 60:
            return f'{obj.duration_seconds:.1f}s'
        else:
            minutes = obj.duration_seconds / 60
            return f'{minutes:.1f}dk'
    duration_display.short_description = 'Süre'
    duration_display.admin_order_field = 'duration_seconds'


# ==============================================================================
# MAÇ VERİLERİ ADMİN
# ==============================================================================

@admin.register(DailyMatchCommentary)
class DailyMatchCommentaryAdmin(admin.ModelAdmin):
    list_display = ['match_display', 'match_date', 'match_time', 'league', 'country', 'created_at']
    list_filter = ['match_date', 'country', 'league']
    search_fields = ['home_team_name', 'away_team_name', 'league', 'country']
    readonly_fields = ['match_id', 'home_team_id', 'away_team_id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Maç Bilgileri', {
            'fields': ('match_id', 'match_date', 'match_time')
        }),
        ('Takımlar', {
            'fields': (('home_team_id', 'home_team_name'), ('away_team_id', 'away_team_name'))
        }),
        ('Lig Bilgileri', {
            'fields': ('country', 'league')
        }),
        ('Commentary', {
            'fields': ('commentary_json',),
            'classes': ('collapse',)
        }),
        ('Diğer', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def match_display(self, obj):
        return f"{obj.home_team_name} vs {obj.away_team_name}"
    match_display.short_description = 'Maç'


@admin.register(ComprehensiveComebackAnalysis)
class ComprehensiveComebackAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'match_display',
        'match_date',
        'combined_score_display',
        'data_quality_badge',
        'created_at'
    ]
    list_filter = ['data_quality', 'match_date']
    search_fields = ['home_team_name', 'away_team_name']
    readonly_fields = ['match_id', 'season_id', 'home_team_id', 'away_team_id', 'created_at']
    
    fieldsets = (
        ('Maç Bilgileri', {
            'fields': ('match_id', 'season_id', 'match_date')
        }),
        ('Takımlar', {
            'fields': (
                ('home_team_id', 'home_team_name', 'home_matches_count'),
                ('away_team_id', 'away_team_name', 'away_matches_count')
            )
        }),
        ('Comeback Skorları', {
            'fields': (
                'home_comeback_score',
                'away_comeback_score',
                'combined_comeback_score',
                'data_quality'
            )
        }),
        ('Commentary', {
            'fields': ('commentary_json',),
            'classes': ('collapse',)
        }),
        ('Diğer', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def match_display(self, obj):
        return f"{obj.home_team_name} vs {obj.away_team_name}"
    match_display.short_description = 'Maç'
    
    def combined_score_display(self, obj):
        """Combined score renkli gösterim"""
        score = obj.combined_comeback_score or 0
        color = 'red' if score >= 15 else 'orange' if score >= 10 else 'green'
        return format_html('<span style="color: {};"><strong>{}</strong></span>', color, f'{score:.1f}')
    combined_score_display.short_description = 'Comeback Score'
    combined_score_display.admin_order_field = 'combined_comeback_score'
    
    def data_quality_badge(self, obj):
        """Data quality badge"""
        if obj.data_quality == 'OK':
            return format_html('<span style="color: green;">✅ OK</span>')
        return format_html('<span style="color: orange;">⚠️ Eksik</span>')
    data_quality_badge.short_description = 'Veri Kalitesi'


@admin.register(LeagueComebackSummary)
class LeagueComebackSummaryAdmin(admin.ModelAdmin):
    list_display = ['league_name', 'season_name', 'match_count', 'created_at']
    list_filter = ['league_name']
    search_fields = ['league_name', 'season_name']
    readonly_fields = ['season_id', 'league_id', 'created_at']


@admin.register(MatchChatHistory)
class MatchChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'user_message_short', 'created_at']
    list_filter = [('created_at', admin.DateFieldListFilter)]
    search_fields = ['match_id', 'user_message', 'ai_response']
    readonly_fields = ['match_id', 'user_message', 'ai_response', 'created_at']
    date_hierarchy = 'created_at'
    
    def user_message_short(self, obj):
        """Kısa mesaj gösterimi"""
        if len(obj.user_message) > 50:
            return obj.user_message[:50] + '...'
        return obj.user_message
    user_message_short.short_description = 'Kullanıcı Mesajı'


# Admin site özelleştirmeleri
admin.site.site_header = 'Spradar Admin Paneli'
admin.site.site_title = 'Spradar Admin'
admin.site.index_title = 'Yönetim Paneli'


# ==============================================================================
# 👤 KULLANICI YÖNETİMİ ADMİN
# ==============================================================================

class UserProfileInline(admin.StackedInline):
    """User admin'e profil ekle"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil Bilgileri'
    fields = [
        'membership_type', 
        'credits', 
        'total_credits_earned', 
        'total_credits_used',
        'is_supervisor',
        ('supervisor_price', 'supervisor_is_active'),
        ('supervisor_bank_name', 'supervisor_iban'),
        'supervisor_account_holder',
        ('supervisor_total_orders', 'supervisor_completed_orders')
    ]
    readonly_fields = ['total_credits_earned', 'total_credits_used', 'supervisor_total_orders', 'supervisor_completed_orders']


class CustomUserAdmin(BaseUserAdmin):
    """Özelleştirilmiş User Admin"""
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'membership_badge', 'credit_display', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'profile__membership_type']
    
    def membership_badge(self, obj):
        """Üyelik tipi badge"""
        if not hasattr(obj, 'profile'):
            return '-'
        
        colors = {
            'FREE': 'gray',
            'GOLD': 'goldenrod',
            'PREMIUM': 'purple',
            'PROFESSIONAL': 'darkblue',
        }
        icons = {
            'FREE': '🆓',
            'GOLD': '🥇',
            'PREMIUM': '💎',
            'PROFESSIONAL': '👑',
        }
        
        member_type = obj.profile.membership_type
        color = colors.get(member_type, 'gray')
        icon = icons.get(member_type, '❓')
        
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{icon} {obj.profile.get_membership_type_display()}</span>'
        )
    membership_badge.short_description = 'Üyelik'
    
    def supervisor_badge(self, obj):
        """Supervisor durumu"""
        if obj.is_supervisor:
            success_rate = obj.get_supervisor_success_rate()
            color = 'green' if success_rate >= 80 else 'orange' if success_rate >= 50 else 'red'
            status = '🟢' if obj.supervisor_is_active else '🔴'
            return format_html(
                '<span style="color: {}; font-weight: bold;">💼 Satıcı {} {:.0f}%</span><br><small>{}/{} sipariş</small>',
                color, status, success_rate,
                obj.supervisor_completed_orders, obj.supervisor_total_orders
            )
        return format_html('<span style="color: gray;">-</span>')
    supervisor_badge.short_description = 'Supervisor'
    
    def credit_display(self, obj):
        """Kredi gösterimi"""
        if not hasattr(obj, 'profile'):
            return '-'
        
        credits = obj.profile.credits
        color = 'green' if credits > 50 else 'orange' if credits > 10 else 'red'
        
        return format_html(f'<span style="color: {color}; font-weight: bold;">{credits} kredi</span>')
    credit_display.short_description = 'Kredi'


# User admin'i yeniden kaydet
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_link',
        'membership_badge',
        'supervisor_badge',
        'credits_display',
        'total_earned_display',
        'total_used_display',
        'usage_rate',
        'created_at_display'
    ]
    list_filter = ['membership_type', 'is_supervisor', 'supervisor_is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'total_credits_earned', 'total_credits_used', 'supervisor_total_orders', 'supervisor_completed_orders']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Kullanıcı', {
            'fields': ('user',)
        }),
        ('Üyelik Bilgileri', {
            'fields': ('membership_type', 'credits')
        }),
        ('💼 Supervisor (Satıcı) Bilgileri', {
            'fields': (
                'is_supervisor',
                'supervisor_price',
                'supervisor_is_active',
                'supervisor_bank_name',
                'supervisor_iban',
                'supervisor_account_holder',
                ('supervisor_total_orders', 'supervisor_completed_orders'),
            ),
            'classes': ('collapse',),
            'description': 'P2P kredi satışı yapan kullanıcılar için özel ayarlar'
        }),
        ('İstatistikler', {
            'fields': ('total_credits_earned', 'total_credits_used'),
            'classes': ('collapse',)
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['add_10_credits', 'add_50_credits', 'add_100_credits', 'upgrade_to_gold', 'upgrade_to_premium', 'upgrade_to_professional', 'make_supervisor', 'remove_supervisor']
    
    def user_link(self, obj):
        """Kullanıcı linki"""
        return format_html(
            '<a href="/admin/auth/user/{}/change/"><strong>{}</strong></a><br><small>{}</small>',
            obj.user.id,
            obj.user.username,
            obj.user.email
        )
    user_link.short_description = 'Kullanıcı'
    
    def membership_badge(self, obj):
        """Üyelik tipi badge"""
        colors = {
            'FREE': 'gray',
            'GOLD': 'goldenrod',
            'PREMIUM': 'purple',
            'PROFESSIONAL': 'darkblue',
        }
        icons = {
            'FREE': '🆓',
            'GOLD': '🥇',
            'PREMIUM': '💎',
            'PROFESSIONAL': '👑',
        }
    def membership_badge(self, obj):
        """Üyelik tipi badge"""
        colors = {
            'FREE': 'gray',
            'GOLD': 'goldenrod',
            'PREMIUM': 'purple',
            'PROFESSIONAL': 'darkblue',
        }
        icons = {
            'FREE': '🆓',
            'GOLD': '🥇',
            'PREMIUM': '💎',
            'PROFESSIONAL': '👑',
        }
        
        color = colors.get(obj.membership_type, 'gray')
        icon = icons.get(obj.membership_type, '❓')
        
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 14px;">{} {}</span>',
            color, icon, obj.get_membership_type_display()
        )
    membership_badge.short_description = 'Üyelik Tipi'
    
    def supervisor_badge(self, obj):
        """Supervisor durumu"""
        if obj.is_supervisor:
            success_rate = obj.get_supervisor_success_rate()
            color = 'green' if success_rate >= 80 else 'orange' if success_rate >= 50 else 'red'
            status = '🟢' if obj.supervisor_is_active else '🔴'
            return format_html(
                '<span style="color: {}; font-weight: bold;">💼 Satıcı {} {}%</span><br><small>{}/{} sipariş</small>',
                color, status, int(success_rate),
                obj.supervisor_completed_orders, obj.supervisor_total_orders
            )
        return format_html('<span style="color: gray;">-</span>')
    supervisor_badge.short_description = 'Supervisor'
    
    def credits_display(self, obj):
        """Kalan kredi"""
        color = 'green' if obj.credits > 50 else 'orange' if obj.credits > 10 else 'red'
        return format_html('<span style="color: {}; font-weight: bold; font-size: 16px;">{}</span>', color, obj.credits)
    credits_display.short_description = 'Kalan Kredi'
    credits_display.admin_order_field = 'credits'
    
    def total_earned_display(self, obj):
        """Toplam kazanılan"""
        return format_html('<span style="color: green;">+{}</span>', obj.total_credits_earned)
    total_earned_display.short_description = 'Toplam Kazanılan'
    
    def total_used_display(self, obj):
        """Toplam kullanılan"""
        return format_html('<span style="color: red;">-{}</span>', obj.total_credits_used)
    total_used_display.short_description = 'Toplam Kullanılan'
    
    def usage_rate(self, obj):
        """Kullanım oranı"""
        if obj.total_credits_earned == 0:
            return '-'
        rate = (obj.total_credits_used / obj.total_credits_earned) * 100
        color = 'red' if rate > 80 else 'orange' if rate > 50 else 'green'
        return format_html('<span style="color: {};">{}</span>', color, f'{rate:.1f}%')
    usage_rate.short_description = 'Kullanım Oranı'
    
    def created_at_display(self, obj):
        """Kayıt tarihi"""
        return obj.created_at.strftime('%d.%m.%Y')
    created_at_display.short_description = 'Kayıt Tarihi'
    created_at_display.admin_order_field = 'created_at'
    
    # Admin Actions
    def add_10_credits(self, request, queryset):
        """10 kredi ekle"""
        for profile in queryset:
            profile.add_credits(10, reason='Admin tarafından eklendi (10 kredi)')
        self.message_user(request, f'{queryset.count()} kullanıcıya 10 kredi eklendi.')
    add_10_credits.short_description = '➕ 10 Kredi Ekle'
    
    def add_50_credits(self, request, queryset):
        """50 kredi ekle"""
        for profile in queryset:
            profile.add_credits(50, reason='Admin tarafından eklendi (50 kredi)')
        self.message_user(request, f'{queryset.count()} kullanıcıya 50 kredi eklendi.')
    add_50_credits.short_description = '➕ 50 Kredi Ekle'
    
    def add_100_credits(self, request, queryset):
        """100 kredi ekle"""
        for profile in queryset:
            profile.add_credits(100, reason='Admin tarafından eklendi (100 kredi)')
        self.message_user(request, f'{queryset.count()} kullanıcıya 100 kredi eklendi.')
    add_100_credits.short_description = '➕ 100 Kredi Ekle'
    
    def upgrade_to_gold(self, request, queryset):
        """Gold üyeliğe yükselt"""
        for profile in queryset:
            profile.upgrade_membership('GOLD')
        self.message_user(request, f'{queryset.count()} kullanıcı Gold üyeliğe yükseltildi.')
    upgrade_to_gold.short_description = '🥇 Gold\'a Yükselt'
    
    def upgrade_to_premium(self, request, queryset):
        """Premium üyeliğe yükselt"""
        for profile in queryset:
            profile.upgrade_membership('PREMIUM')
        self.message_user(request, f'{queryset.count()} kullanıcı Premium üyeliğe yükseltildi.')
    upgrade_to_premium.short_description = '💎 Premium\'a Yükselt'
    
    def upgrade_to_professional(self, request, queryset):
        """Professional üyeliğe yükselt"""
        for profile in queryset:
            profile.upgrade_membership('PROFESSIONAL')
        self.message_user(request, f'{queryset.count()} kullanıcı Professional üyeliğe yükseltildi.')
    upgrade_to_professional.short_description = '👑 Professional\'a Yükselt'
    
    def make_supervisor(self, request, queryset):
        """Supervisor yap"""
        count = queryset.update(is_supervisor=True, supervisor_is_active=True)
        self.message_user(request, f'{count} kullanıcı Supervisor olarak işaretlendi.')
    make_supervisor.short_description = '💼 Supervisor Yap'
    
    def remove_supervisor(self, request, queryset):
        """Supervisor kaldır"""
        count = queryset.update(is_supervisor=False, supervisor_is_active=False)
        self.message_user(request, f'{count} kullanıcının Supervisor yetkisi kaldırıldı.')
    remove_supervisor.short_description = '🚫 Supervisor Kaldır'



@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'created_at_display',
        'user_link',
        'transaction_badge',
        'amount_display',
        'balance_display',
        'reason'
    ]
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user_profile__user__username', 'reason']
    readonly_fields = ['user_profile', 'transaction_type', 'amount', 'balance_after', 'reason', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        """Manuel transaction eklemeyi engelle"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Transaction değiştirmeyi engelle"""
        return False
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Tarih/Saat'
    created_at_display.admin_order_field = 'created_at'
    
    def user_link(self, obj):
        """Kullanıcı linki"""
        return format_html(
            '<a href="/admin/api/userprofile/{}/change/">{}</a>',
            obj.user_profile.id,
            obj.user_profile.user.username
        )
    user_link.short_description = 'Kullanıcı'
    
    def transaction_badge(self, obj):
        """İşlem tipi badge"""
        if obj.transaction_type == 'CREDIT':
            return format_html('<span style="color: green; font-weight: bold;">➕ Ekleme</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">➖ Kullanım</span>')
    transaction_badge.short_description = 'İşlem Tipi'
    
    def amount_display(self, obj):
        """Miktar gösterimi"""
        symbol = '+' if obj.transaction_type == 'CREDIT' else '-'
        color = 'green' if obj.transaction_type == 'CREDIT' else 'red'
        return format_html('<span style="color: {}; font-weight: bold;">{}{}</span>', color, symbol, obj.amount)
    amount_display.short_description = 'Miktar'
    
    def balance_display(self, obj):
        """Bakiye gösterimi"""
        return format_html('<strong>{}</strong>', obj.balance_after)
    balance_display.short_description = 'Sonraki Bakiye'


@admin.register(CommentHistory)
class CommentHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'created_at_display',
        'user_link',
        'match_info_short',
        'question_short',
        'credits_used',
    ]
    list_filter = ['created_at', 'credits_used']
    search_fields = ['user__username', 'match_info', 'user_question']
    readonly_fields = ['user', 'match_id', 'match_info', 'user_question', 'ai_response', 'credits_used', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Kullanıcı ve Maç', {
            'fields': ('user', 'match_id', 'match_info', 'created_at')
        }),
        ('Konuşma', {
            'fields': ('user_question', 'ai_response')
        }),
        ('Kredi', {
            'fields': ('credits_used',)
        }),
    )
    
    def has_add_permission(self, request):
        """Manuel yorum eklemeyi engelle"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Yorum değiştirmeyi engelle"""
        return False
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Tarih/Saat'
    created_at_display.admin_order_field = 'created_at'
    
    def user_link(self, obj):
        """Kullanıcı linki"""
        return format_html(
            '<a href="/admin/api/userprofile/?user__id__exact={}">{}</a>',
            obj.user.id,
            obj.user.username
        )
    user_link.short_description = 'Kullanıcı'
    
    def match_info_short(self, obj):
        """Kısa maç bilgisi"""
        if obj.match_info and len(obj.match_info) > 40:
            return obj.match_info[:40] + '...'
        return obj.match_info or f'Maç #{obj.match_id}'
    match_info_short.short_description = 'Maç'
    
    def question_short(self, obj):
        """Kısa soru gösterimi"""
        if len(obj.user_question) > 50:
            return obj.user_question[:50] + '...'
        return obj.user_question
    question_short.short_description = 'Soru'


@admin.register(CreditPurchase)
class CreditPurchaseAdmin(admin.ModelAdmin):
    list_display = [
        'created_at_display',
        'user_link',
        'payment_code_display',
        'credit_amount_display',
        'price_display',
        'status_badge',
        'approved_by_display'
    ]
    list_filter = ['payment_status', 'created_at']
    search_fields = ['user_profile__user__username', 'payment_note', 'payment_code']
    readonly_fields = ['user_profile', 'credit_amount', 'price', 'payment_code', 'created_at', 'approved_at', 'approved_by']
    date_hierarchy = 'created_at'
    actions = ['approve_purchase', 'reject_purchase']
    
    fieldsets = (
        ('Sipariş Bilgileri', {
            'fields': ('user_profile', 'credit_amount', 'price', 'payment_code', 'payment_status')
        }),
        ('Ödeme Detayları', {
            'fields': ('payment_note',)
        }),
        ('Onay Bilgileri', {
            'fields': ('approved_at', 'approved_by'),
            'classes': ('collapse',)
        }),
        ('Tarihler', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Sipariş Tarihi'
    created_at_display.admin_order_field = 'created_at'
    
    def user_link(self, obj):
        """Kullanıcı linki"""
        return format_html(
            '<a href="/admin/api/userprofile/{}/change/">{}</a>',
            obj.user_profile.id,
            obj.user_profile.user.username
        )
    user_link.short_description = 'Kullanıcı'
    
    def payment_code_display(self, obj):
        """Ödeme kodu gösterimi"""
        if obj.payment_code:
            return format_html(
                '<code style="background: #f0f0f0; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 1.1em;">{}</code>',
                obj.payment_code
            )
        return '-'
    payment_code_display.short_description = 'Ödeme Kodu'
    
    def credit_amount_display(self, obj):
        """Kredi miktarı gösterimi"""
        formatted_amount = f'{obj.credit_amount:,}'.replace(',', '.')
        return format_html('<strong>{}</strong> Kredi', formatted_amount)
    credit_amount_display.short_description = 'Miktar'
    
    def price_display(self, obj):
        """Fiyat gösterimi"""
        formatted_price = f'{obj.price:.2f}'.replace('.', ',')
        return format_html('<strong>{}</strong> ₺', formatted_price)
    price_display.short_description = 'Fiyat'
    
    def status_badge(self, obj):
        """Durum badge"""
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'blue',
            'REJECTED': 'red',
            'COMPLETED': 'green',
        }
        icons = {
            'PENDING': '⏳',
            'APPROVED': '✅',
            'REJECTED': '❌',
            'COMPLETED': '🎉',
        }
        color = colors.get(obj.payment_status, 'gray')
        icon = icons.get(obj.payment_status, '❓')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_payment_status_display()
        )
    status_badge.short_description = 'Durum'
    
    def approved_by_display(self, obj):
        """Onaylayan admin gösterimi"""
        if obj.approved_by:
            return obj.approved_by.username
        return '-'
    approved_by_display.short_description = 'Onaylayan'
    
    def approve_purchase(self, request, queryset):
        """Siparişleri onayla ve kredileri ekle"""
        from django.utils import timezone
        
        approved_count = 0
        for purchase in queryset.filter(payment_status='PENDING'):
            # Durumu onayla
            purchase.payment_status = 'COMPLETED'
            purchase.approved_at = timezone.now()
            purchase.approved_by = request.user
            purchase.save()
            
            # Kullanıcıya kredi ekle
            purchase.user_profile.add_credits(
                purchase.credit_amount,
                reason=f'Kredi satın alma: {purchase.credit_amount} Kredi ({purchase.price} TL)'
            )
            approved_count += 1
        
        self.message_user(request, f'{approved_count} sipariş onaylandı ve krediler eklendi.')
    approve_purchase.short_description = '✅ Seçili siparişleri onayla ve kredi ekle'
    
    def reject_purchase(self, request, queryset):
        """Siparişleri reddet"""
        from django.utils import timezone
        
        rejected_count = queryset.filter(payment_status='PENDING').update(
            payment_status='REJECTED',
            approved_at=timezone.now(),
            approved_by=request.user
        )
        self.message_user(request, f'{rejected_count} sipariş reddedildi.')
    reject_purchase.short_description = '❌ Seçili siparişleri reddet'


@admin.register(SupervisorCreditPurchase)
class SupervisorCreditPurchaseAdmin(admin.ModelAdmin):
    """P2P Kredi Satış Siparişleri (Supervisor → Kullanıcı)"""
    list_display = [
        'created_at_display',
        'buyer_link',
        'supervisor_link',
        'payment_code_display',
        'credit_amount_display',
        'total_price_display',
        'status_badge',
        'completed_at_display'
    ]
    list_filter = ['payment_status', 'created_at', 'supervisor']
    search_fields = [
        'buyer__user__username',
        'supervisor__user__username',
        'payment_code',
        'payment_note',
        'supervisor_note'
    ]
    readonly_fields = [
        'buyer',
        'supervisor',
        'credit_amount',
        'unit_price',
        'total_price',
        'payment_code',
        'created_at',
        'completed_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('P2P Sipariş Bilgileri', {
            'fields': (
                ('buyer', 'supervisor'),
                'credit_amount',
                ('unit_price', 'total_price'),
                'payment_code',
                'payment_status'
            )
        }),
        ('Ödeme Detayları', {
            'fields': ('payment_note',)
        }),
        ('Supervisor Notu', {
            'fields': ('supervisor_note',)
        }),
        ('Tarihler', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Sipariş Tarihi'
    created_at_display.admin_order_field = 'created_at'
    
    def completed_at_display(self, obj):
        """Tamamlanma tarihi"""
        if obj.completed_at:
            return obj.completed_at.strftime('%d.%m.%Y %H:%M')
        return '-'
    completed_at_display.short_description = 'Tamamlanma'
    
    def buyer_link(self, obj):
        """Alıcı linki"""
        return format_html(
            '<a href="/admin/api/userprofile/{}/change/">👤 {}</a><br><small>{} kredi</small>',
            obj.buyer.id,
            obj.buyer.user.username,
            obj.buyer.credits
        )
    buyer_link.short_description = 'Alıcı'
    
    def supervisor_link(self, obj):
        """Satıcı linki"""
        success_rate = obj.supervisor.get_supervisor_success_rate()
        # Önce format yap, sonra format_html kullan (SafeString çakışması önlenir)
        rate_text = f'{success_rate:.0f}%'
        return format_html(
            '<a href="/admin/api/userprofile/{}/change/">💼 {}</a><br><small>{}/{} ({})</small>',
            obj.supervisor.id,
            obj.supervisor.user.username,
            obj.supervisor.supervisor_completed_orders,
            obj.supervisor.supervisor_total_orders,
            rate_text
        )
    supervisor_link.short_description = 'Satıcı (Supervisor)'
    
    def payment_code_display(self, obj):
        """Ödeme kodu"""
        if obj.payment_code:
            return format_html(
                '<code style="background: #e8f5e9; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</code>',
                obj.payment_code
            )
        return '-'
    payment_code_display.short_description = 'Ödeme Kodu'
    
    def credit_amount_display(self, obj):
        """Kredi miktarı"""
        formatted = f'{obj.credit_amount:,}'.replace(',', '.')
        return format_html('<strong>{}</strong> Kredi', formatted)
    credit_amount_display.short_description = 'Miktar'
    
    def total_price_display(self, obj):
        """Toplam fiyat"""
        # Önce format yap (SafeString çakışması önlenir)
        total_price_formatted = f'{obj.total_price:.2f}'
        unit_price_formatted = f'{obj.unit_price:.2f}'
        return format_html(
            '<strong style="color: green;">{} ₺</strong><br><small>{} ₺/kredi</small>',
            total_price_formatted, unit_price_formatted
        )
    total_price_display.short_description = 'Fiyat'
    
    def status_badge(self, obj):
        """Durum badge"""
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'green',
            'REJECTED': 'red',
            'CANCELLED': 'gray',
        }
        icons = {
            'PENDING': '⏳',
            'APPROVED': '✅',
            'REJECTED': '❌',
            'CANCELLED': '🚫',
        }
        color = colors.get(obj.payment_status, 'gray')
        icon = icons.get(obj.payment_status, '❓')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_payment_status_display()
        )
    status_badge.short_description = 'Durum'
    
    def save_model(self, request, obj, form, change):
        """
        Admin panelinden kaydedildiğinde otomatik işlemler
        Eğer durumu PENDING'den APPROVED'a çeviriyorsa, kredi ekle
        """
        if change:  # Mevcut kayıt güncelleniyor
            # Önceki durumu al
            old_obj = SupervisorCreditPurchase.objects.get(pk=obj.pk)
            old_status = old_obj.payment_status
            new_status = obj.payment_status
            
            # PENDING → APPROVED: Onaylama işlemi
            if old_status == 'PENDING' and new_status == 'APPROVED':
                # Model'deki approve_order() metodunu çağır
                success, message = obj.approve_order()
                
                if success:
                    self.message_user(request, f'✅ {message}', level='success')
                else:
                    self.message_user(request, f'❌ {message}', level='error')
                return  # approve_order() zaten save() yapıyor
            
            # PENDING/APPROVED → REJECTED: Reddetme işlemi
            elif old_status in ['PENDING', 'APPROVED'] and new_status == 'REJECTED':
                # Model'deki reject_order() metodunu çağır
                reason = obj.rejection_reason or 'Admin tarafından reddedildi'
                success, message = obj.reject_order(reason)
                
                if success:
                    self.message_user(request, f'❌ {message}', level='warning')
                else:
                    self.message_user(request, f'❌ {message}', level='error')
                return  # reject_order() zaten save() yapıyor
        
        # Normal kayıt
        super().save_model(request, obj, form, change)


@admin.register(SupervisorApplication)
class SupervisorApplicationAdmin(admin.ModelAdmin):
    """Supervisor Başvuru Yönetimi"""
    list_display = [
        'created_at_display',
        'user_link',
        'bank_info_display',
        'proposed_price_display',
        'status_badge',
        'reviewed_by_display'
    ]
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = [
        'user_profile__user__username',
        'user_profile__user__email',
        'bank_name',
        'iban',
        'account_holder'
    ]
    readonly_fields = [
        'user_profile',
        'bank_name',
        'iban',
        'account_holder',
        'proposed_price',
        'description',
        'created_at',
        'reviewed_at',
        'reviewed_by'
    ]
    date_hierarchy = 'created_at'
    actions = ['approve_applications', 'reject_applications', 'delete_selected_applications']
    
    def get_actions(self, request):
        """Django'nun varsayılan delete action'ını kaldırıp kendi action'ımızı kullan"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    fieldsets = (
        ('Başvuru Sahibi', {
            'fields': ('user_profile', 'created_at')
        }),
        ('Banka Bilgileri', {
            'fields': ('bank_name', 'iban', 'account_holder', 'proposed_price')
        }),
        ('Açıklama', {
            'fields': ('description',)
        }),
        ('Durum', {
            'fields': ('status', 'admin_note')
        }),
        ('İnceleme Bilgileri', {
            'fields': ('reviewed_at', 'reviewed_by'),
            'classes': ('collapse',)
        }),
    )
    
    def created_at_display(self, obj):
        """Başvuru tarihi"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Başvuru Tarihi'
    created_at_display.admin_order_field = 'created_at'
    
    def user_link(self, obj):
        """Kullanıcı bilgisi"""
        return format_html(
            '<a href="/admin/api/userprofile/{}/change/">👤 {}</a><br><small>{}</small>',
            obj.user_profile.id,
            obj.user_profile.user.username,
            obj.user_profile.user.email
        )
    user_link.short_description = 'Kullanıcı'
    
    def bank_info_display(self, obj):
        """Banka bilgileri"""
        return format_html(
            '<strong>{}</strong><br><small>{}</small><br><small>{}</small>',
            obj.bank_name,
            obj.iban,
            obj.account_holder
        )
    bank_info_display.short_description = 'Banka Bilgileri'
    
    def proposed_price_display(self, obj):
        """Önerilen fiyat"""
        return format_html(
            '<strong style="color: green;">{} ₺</strong><br><small>/ kredi</small>',
            f'{float(obj.proposed_price):.2f}'
        )
    proposed_price_display.short_description = 'Önerilen Fiyat'
    
    def status_badge(self, obj):
        """Durum badge"""
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'green',
            'REJECTED': 'red',
        }
        icons = {
            'PENDING': '⏳',
            'APPROVED': '✅',
            'REJECTED': '❌',
        }
        color = colors.get(obj.status, 'gray')
        icon = icons.get(obj.status, '❓')
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 1.1em;">{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = 'Durum'
    
    def reviewed_by_display(self, obj):
        """İnceleyen admin"""
        if obj.reviewed_by:
            return format_html(
                '{}<br><small>{}</small>',
                obj.reviewed_by.username,
                obj.reviewed_at.strftime('%d.%m.%Y') if obj.reviewed_at else ''
            )
        return '-'
    reviewed_by_display.short_description = 'İnceleyen'
    
    def approve_applications(self, request, queryset):
        """Başvuruları onayla"""
        approved_count = 0
        for application in queryset.filter(status='PENDING'):
            success, message = application.approve(request.user, note='Admin tarafından onaylandı')
            if success:
                approved_count += 1
        
        self.message_user(
            request,
            f'✅ {approved_count} başvuru onaylandı ve kullanıcılar supervisor oldu!'
        )
    approve_applications.short_description = '✅ Seçili başvuruları onayla (Supervisor yap)'
    
    def reject_applications(self, request, queryset):
        """Başvuruları reddet"""
        rejected_count = 0
        for application in queryset.filter(status='PENDING'):
            success, message = application.reject(request.user, note='Admin tarafından reddedildi')
            if success:
                rejected_count += 1
        
        self.message_user(request, f'❌ {rejected_count} başvuru reddedildi.')
    reject_applications.short_description = '❌ Seçili başvuruları reddet'
    
    def delete_selected_applications(self, request, queryset):
        """Başvuruları sil ve supervisor yetkilerini kaldır"""
        deleted_count = 0
        for application in queryset:
            user_profile = application.user_profile
            username = user_profile.user.username
            
            # Eğer onaylanmış başvuru ise, supervisor yetkilerini kaldır
            if application.status == 'APPROVED' and user_profile.is_supervisor:
                user_profile.is_supervisor = False
                user_profile.supervisor_is_active = False
                user_profile.save()
                self.message_user(
                    request, 
                    f'⚠️ {username} kullanıcısının supervisor yetkileri kaldırıldı.',
                    level='warning'
                )
            
            # Başvuruyu sil
            application.delete()
            deleted_count += 1
        
        self.message_user(
            request,
            f'🗑️ {deleted_count} başvuru silindi ve ilgili kullanıcıların supervisor yetkileri kaldırıldı.'
        )
    delete_selected_applications.short_description = '🗑️ Seçili başvuruları sil (Supervisor yetkilerini kaldır)'
    
    def delete_model(self, request, obj):
        """Tekli silme işlemi - supervisor yetkilerini kaldır"""
        user_profile = obj.user_profile
        
        # Eğer onaylanmış başvuru ise, supervisor yetkilerini kaldır
        if obj.status == 'APPROVED' and user_profile.is_supervisor:
            user_profile.is_supervisor = False
            user_profile.supervisor_is_active = False
            user_profile.save()
            self.message_user(
                request, 
                f'⚠️ {user_profile.user.username} kullanıcısının supervisor yetkileri kaldırıldı.',
                level='warning'
            )
        
        # Başvuruyu sil
        super().delete_model(request, obj)
        self.message_user(request, f'🗑️ Başvuru silindi.')
    
    def delete_queryset(self, request, queryset):
        """Toplu silme işlemi - supervisor yetkilerini kaldır"""
        for application in queryset:
            user_profile = application.user_profile
            
            # Eğer onaylanmış başvuru ise, supervisor yetkilerini kaldır
            if application.status == 'APPROVED' and user_profile.is_supervisor:
                user_profile.is_supervisor = False
                user_profile.supervisor_is_active = False
                user_profile.save()
        
        # Başvuruları sil
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'🗑️ {count} başvuru silindi ve ilgili kullanıcıların supervisor yetkileri kaldırıldı.')


@admin.register(CreditTransfer)
class CreditTransferAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user_link', 'to_user_link', 'amount', 'note', 'created_at_display']
    list_filter = ['created_at']
    search_fields = ['from_user__user__username', 'to_user__user__username', 'note']
    readonly_fields = ['from_user', 'to_user', 'amount', 'note', 'created_at']
    date_hierarchy = 'created_at'
    
    def from_user_link(self, obj):
        """Gönderen kullanıcı linki"""
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:api_userprofile_change', args=[obj.from_user.pk])
        return format_html('<a href="{}">{}</a> ({} kredi)', url, obj.from_user.user.username, obj.from_user.credits)
    from_user_link.short_description = 'Gönderen'
    
    def to_user_link(self, obj):
        """Alıcı kullanıcı linki"""
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:api_userprofile_change', args=[obj.to_user.pk])
        return format_html('<a href="{}">{}</a> ({} kredi)', url, obj.to_user.user.username, obj.to_user.credits)
    to_user_link.short_description = 'Alıcı'
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        from django.utils.html import format_html
        return format_html('{}', obj.created_at.strftime('%d.%m.%Y %H:%M'))
    created_at_display.short_description = 'Transfer Tarihi'


# ==============================================================================
# 💬 DESTEK SİSTEMİ ADMIN
# ==============================================================================

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_link', 'subject', 'category', 'status_badge', 'priority_badge', 'created_at_display', 'action_buttons']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['user__username', 'subject', 'message']
    readonly_fields = ['user', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Talep Bilgileri', {
            'fields': ['user', 'subject', 'category', 'message', 'priority', 'status']
        }),
        ('Admin Cevabı', {
            'fields': ['admin_response', 'responded_by', 'responded_at']
        }),
        ('Tarihler', {
            'fields': ['created_at', 'updated_at']
        }),
    ]
    
    actions = ['mark_as_in_progress', 'mark_as_closed']
    
    def user_link(self, obj):
        """Kullanıcı linki"""
        from django.urls import reverse
        url = reverse('admin:api_userprofile_change', args=[obj.user.profile.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'Kullanıcı'
    
    def status_badge(self, obj):
        """Durum badge'i"""
        colors = {
            'OPEN': 'red',
            'IN_PROGRESS': 'orange',
            'CLOSED': 'green'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Durum'
    
    def priority_badge(self, obj):
        """Öncelik badge'i"""
        colors = {
            'LOW': '#28a745',
            'MEDIUM': '#ffc107',
            'HIGH': '#fd7e14',
            'URGENT': '#dc3545'
        }
        color = colors.get(obj.priority, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = 'Öncelik'
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Tarih'
    
    def action_buttons(self, obj):
        """Hızlı aksiyon butonları"""
        buttons = []
        if obj.status == 'OPEN':
            buttons.append(f'<span style="color: orange;">⏳ Beklemede</span>')
        elif obj.status == 'IN_PROGRESS':
            buttons.append(f'<span style="color: blue;">✍️ Cevaplanıyor</span>')
        else:
            buttons.append(f'<span style="color: green;">✅ Kapatıldı</span>')
        return format_html(' '.join(buttons))
    action_buttons.short_description = 'Durum'
    
    def save_model(self, request, obj, form, change):
        """Admin cevabı eklendiğinde otomatik işlemler"""
        if change and obj.admin_response and not obj.responded_by:
            obj.responded_by = request.user
            obj.responded_at = timezone.now()
            obj.status = 'IN_PROGRESS'
        super().save_model(request, obj, form, change)
    
    def mark_as_in_progress(self, request, queryset):
        """Toplu cevaplanıyor olarak işaretle"""
        updated = queryset.update(status='IN_PROGRESS')
        self.message_user(request, f'{updated} talep cevaplanıyor olarak işaretlendi.')
    mark_as_in_progress.short_description = '✍️ Cevaplanıyor olarak işaretle'
    
    def mark_as_closed(self, request, queryset):
        """Toplu kapatma"""
        updated = queryset.update(status='CLOSED')
        self.message_user(request, f'{updated} talep kapatıldı.')
    mark_as_closed.short_description = '✅ Kapat'


# ==============================================================================
# 📢 DUYURU SİSTEMİ ADMIN
# ==============================================================================

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type_badge', 'is_active', 'is_pinned', 'date_range', 'created_by', 'created_at_display']
    list_filter = ['announcement_type', 'is_active', 'is_pinned', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Duyuru Bilgileri', {
            'fields': ['title', 'content', 'announcement_type']
        }),
        ('Görünürlük', {
            'fields': ['is_active', 'is_pinned', 'start_date', 'end_date']
        }),
        ('Meta', {
            'fields': ['created_by', 'created_at', 'updated_at']
        }),
    ]
    
    actions = ['activate_announcements', 'deactivate_announcements', 'pin_announcements']
    
    def save_model(self, request, obj, form, change):
        """Oluşturan kullanıcıyı kaydet"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def type_badge(self, obj):
        """Tip badge'i"""
        colors = {
            'INFO': '#17a2b8',
            'SUCCESS': '#28a745',
            'WARNING': '#ffc107',
            'DANGER': '#dc3545'
        }
        color = colors.get(obj.announcement_type, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_announcement_type_display()
        )
    type_badge.short_description = 'Tip'
    
    def date_range(self, obj):
        """Tarih aralığı"""
        if obj.start_date or obj.end_date:
            start = obj.start_date.strftime('%d.%m.%Y') if obj.start_date else '∞'
            end = obj.end_date.strftime('%d.%m.%Y') if obj.end_date else '∞'
            return format_html('{} → {}', start, end)
        return '-'
    date_range.short_description = 'Geçerlilik'
    
    def created_at_display(self, obj):
        """Tarih formatı"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = 'Oluşturulma'
    
    def activate_announcements(self, request, queryset):
        """Toplu aktifleştirme"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} duyuru aktif edildi.')
    activate_announcements.short_description = '✅ Aktif Et'
    
    def deactivate_announcements(self, request, queryset):
        """Toplu pasifleştirme"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} duyuru pasif edildi.')
    deactivate_announcements.short_description = '❌ Pasif Et'
    
    def pin_announcements(self, request, queryset):
        """Toplu sabitleme"""
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f'{updated} duyuru sabitlendi.')
    pin_announcements.short_description = '📌 Sabitle'


@admin.register(UserAnnouncementRead)
class UserAnnouncementReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'announcement', 'read_at']
    list_filter = ['read_at']
    search_fields = ['user__username', 'announcement__title']
    readonly_fields = ['user', 'announcement', 'read_at']



