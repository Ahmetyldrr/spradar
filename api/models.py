"""
🎯 Django Models - Mevcut PostgreSQL tablolarını temsil eder
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class LeagueComebackSummary(models.Model):
    """
    league_comeback_summary tablosu için Django model
    """
    season_id = models.IntegerField(primary_key=True)
    season_name = models.TextField(blank=True, null=True)
    league_name = models.TextField(blank=True, null=True)
    league_id = models.IntegerField(blank=True, null=True)
    match_count = models.IntegerField(blank=True, null=True)
    matches_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False  # Django migrations çalıştırmasın, tablo zaten var
        db_table = 'league_comeback_summary'
        ordering = ['-match_count']

    def __str__(self):
        return f"{self.league_name} - Season {self.season_id} ({self.match_count} matches)"


class DailyMatchCommentary(models.Model):
    """
    daily_match_commentaries tablosu için Django model
    """
    match_id = models.BigIntegerField(primary_key=True)
    match_date = models.CharField(max_length=50)  # Veritabanında VARCHAR
    match_time = models.CharField(max_length=10, blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    league = models.TextField(blank=True, null=True)
    home_team_id = models.IntegerField()
    home_team_name = models.TextField()
    away_team_id = models.IntegerField()
    away_team_name = models.TextField()
    commentary_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False  # Django migrations çalıştırmasın
        db_table = 'daily_match_commentaries'
        ordering = ['match_date', 'match_time']

    def __str__(self):
        return f"{self.home_team_name} vs {self.away_team_name} ({self.match_date})"
    
    def get_friendly_url(self):
        """SEO-friendly URL oluştur"""
        from django.utils.text import slugify
        return f"/matches/{slugify(self.country or 'other')}/{slugify(self.league or 'general')}/{slugify(self.home_team_name)}/{slugify(self.away_team_name)}/"


class ComprehensiveComebackAnalysis(models.Model):
    """
    comprehensive_comeback_analysis tablosu için Django model
    """
    match_id = models.BigIntegerField(primary_key=True)
    season_id = models.IntegerField(blank=True, null=True)
    match_date = models.CharField(max_length=50, blank=True, null=True)
    home_team_id = models.IntegerField()
    home_team_name = models.TextField()
    away_team_id = models.IntegerField()
    away_team_name = models.TextField()
    home_matches_count = models.IntegerField(blank=True, null=True)
    away_matches_count = models.IntegerField(blank=True, null=True)
    home_comeback_score = models.FloatField(blank=True, null=True)
    away_comeback_score = models.FloatField(blank=True, null=True)
    combined_comeback_score = models.FloatField(blank=True, null=True)
    data_quality = models.CharField(max_length=20, blank=True, null=True)
    commentary_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'comprehensive_comeback_analysis'
        ordering = ['-combined_comeback_score']

    def __str__(self):
        return f"{self.home_team_name} vs {self.away_team_name} (Score: {self.combined_comeback_score})"


class MatchChatHistory(models.Model):
    """
    Maç bazlı AI chat geçmişi - Kullanıcıya özel
    """
    match_id = models.BigIntegerField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_chats', null=True, blank=True)  # Eski kayıtlar için null
    user_message = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'match_chat_history'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['match_id', 'user', 'created_at']),
        ]
    
    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"Chat for Match {self.match_id} by {username} at {self.created_at}"


class CronService(models.Model):
    """
    Cron servisleri tablosu - Fixture2X, Commentary, Comeback gibi servisler
    """
    SERVICE_TYPES = [
        ('FIXTURE2X', 'Fixture 2X'),
        ('COMMENTARY', 'Commentary'),
        ('COMEBACK', 'Comeback Analysis'),
        ('SRSERVICE', 'SR Service'),
        ('OTHER', 'Diğer'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Servis Adı')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, verbose_name='Servis Tipi')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    cron_schedule = models.CharField(max_length=50, blank=True, verbose_name='Cron Zamanı', help_text='Örn: 30 5 * * *')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    last_run = models.DateTimeField(null=True, blank=True, verbose_name='Son Çalışma')
    last_status = models.BooleanField(null=True, blank=True, verbose_name='Son Durum')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme')
    
    class Meta:
        db_table = 'cron_services'
        ordering = ['name']
        verbose_name = 'Cron Servisi'
        verbose_name_plural = 'Cron Servisleri'
    
    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"


class ServiceLog(models.Model):
    """
    Servis işlem logları - Her servis çalıştığında kayıt oluşur
    """
    STATUS_CHOICES = [
        ('SUCCESS', 'Başarılı'),
        ('ERROR', 'Hata'),
        ('WARNING', 'Uyarı'),
        ('INFO', 'Bilgi'),
    ]
    
    service = models.ForeignKey(
        CronService, 
        on_delete=models.CASCADE, 
        related_name='logs',
        verbose_name='Servis'
    )
    operation_name = models.CharField(max_length=200, verbose_name='İşlem Adı')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Durum')
    message = models.TextField(blank=True, verbose_name='Mesaj')
    details = models.JSONField(null=True, blank=True, verbose_name='Detaylar')
    duration_seconds = models.FloatField(null=True, blank=True, verbose_name='Süre (saniye)')
    processed_count = models.IntegerField(null=True, blank=True, verbose_name='İşlenen Sayı')
    error_count = models.IntegerField(null=True, blank=True, verbose_name='Hata Sayısı')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma', db_index=True)
    
    class Meta:
        db_table = 'service_logs'
        ordering = ['-created_at']
        verbose_name = 'Servis Logu'
        verbose_name_plural = 'Servis Logları'
        indexes = [
            models.Index(fields=['service', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.service.name} - {self.operation_name} ({self.get_status_display()})"
    
    @property
    def status_icon(self):
        """Admin panelinde görsel gösterim için"""
        icons = {
            'SUCCESS': '✅',
            'ERROR': '❌',
            'WARNING': '⚠️',
            'INFO': 'ℹ️',
        }
        return icons.get(self.status, '❓')


# ==============================================================================
# 👤 USER MANAGEMENT & CREDIT SYSTEM
# ==============================================================================

class UserProfile(models.Model):
    """
    Kullanıcı profili - Kredi ve üyelik sistemi
    """
    MEMBERSHIP_TYPES = [
        ('FREE', 'Ücretsiz (10 Kredi)'),
        ('GOLD', 'Gold (100 Kredi)'),
        ('PREMIUM', 'Premium (1.000 Kredi)'),
        ('PROFESSIONAL', 'Professional (10.000 Kredi)'),
    ]
    
    CREDIT_PACKAGES = {
        'FREE': 10,
        'GOLD': 100,
        'PREMIUM': 1000,
        'PROFESSIONAL': 10000,
    }
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='Kullanıcı'
    )
    membership_type = models.CharField(
        max_length=20, 
        choices=MEMBERSHIP_TYPES, 
        default='FREE',
        verbose_name='Üyelik Tipi'
    )
    credits = models.IntegerField(default=10, verbose_name='Kalan Kredi')
    total_credits_earned = models.IntegerField(default=10, verbose_name='Toplam Kazanılan Kredi')
    total_credits_used = models.IntegerField(default=0, verbose_name='Toplam Kullanılan Kredi')
    
    # 🎯 Supervisor (P2P Satıcı) Alanları
    is_supervisor = models.BooleanField(default=False, verbose_name='Satıcı mı?', help_text='P2P kredi satışı yapabilir')
    supervisor_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.35,
        verbose_name='Satış Fiyatı (TL)',
        help_text='Supervisor kredilerini bu fiyattan satar (Admin 0.29 TL\'ye satar)'
    )
    supervisor_bank_name = models.CharField(max_length=100, blank=True, verbose_name='Banka Adı')
    supervisor_iban = models.CharField(max_length=34, blank=True, verbose_name='IBAN')
    supervisor_account_holder = models.CharField(max_length=200, blank=True, verbose_name='Hesap Sahibi')
    supervisor_total_orders = models.IntegerField(default=0, verbose_name='Toplam Sipariş', help_text='Alınan toplam sipariş sayısı')
    supervisor_completed_orders = models.IntegerField(default=0, verbose_name='Tamamlanan Sipariş', help_text='Onaylanan sipariş sayısı')
    supervisor_is_active = models.BooleanField(default=True, verbose_name='Satıcı Aktif mi?', help_text='Listeye çıksın mı?')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Son Güncelleme')
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Kullanıcı Profili'
        verbose_name_plural = 'Kullanıcı Profilleri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_membership_type_display()} ({self.credits} kredi)"
    
    def add_credits(self, amount, reason='Manuel ekleme'):
        """Kredi ekle"""
        self.credits += amount
        self.total_credits_earned += amount
        self.save()
        
        # Log oluştur
        CreditTransaction.objects.create(
            user_profile=self,
            transaction_type='CREDIT',
            amount=amount,
            balance_after=self.credits,
            reason=reason
        )
    
    def deduct_credits(self, amount, reason='AI yorum'):
        """Kredi düş"""
        if self.credits >= amount:
            self.credits -= amount
            self.total_credits_used += amount
            self.save()
            
            # Log oluştur
            CreditTransaction.objects.create(
                user_profile=self,
                transaction_type='DEBIT',
                amount=amount,
                balance_after=self.credits,
                reason=reason
            )
            return True
        return False
    
    def has_credits(self, amount=1):
        """Yeterli kredi var mı?"""
        return self.credits >= amount
    
    def upgrade_membership(self, new_type):
        """Üyelik tipini yükselt ve kredi ekle"""
        if new_type in self.CREDIT_PACKAGES:
            old_type = self.membership_type
            self.membership_type = new_type
            self.save()  # Üyelik tipini kaydet
            credit_amount = self.CREDIT_PACKAGES[new_type]
            
            self.add_credits(
                credit_amount,
                reason=f'Üyelik yükseltme: {old_type} → {new_type}'
            )
    
    def get_supervisor_success_rate(self):
        """Supervisor başarı oranını hesapla"""
        if not self.is_supervisor or self.supervisor_total_orders == 0:
            return 0
        return round((self.supervisor_completed_orders / self.supervisor_total_orders) * 100, 1)
    
    def can_sell_credits(self, amount):
        """Supervisor yeterli krediye sahip mi? (satış için)"""
        return self.is_supervisor and self.credits >= amount


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Yeni kullanıcı oluşturulduğunda otomatik profil oluştur"""
    if created:
        # get_or_create kullanarak duplicate hatası önleniyor
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={
                'membership_type': 'FREE',
                'credits': 10,
                'total_credits_earned': 10
            }
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Kullanıcı kaydedildiğinde profili de kaydet"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class CreditTransaction(models.Model):
    """
    Kredi işlem geçmişi
    """
    TRANSACTION_TYPES = [
        ('CREDIT', 'Kredi Ekleme (+)'),
        ('DEBIT', 'Kredi Kullanma (-)'),
    ]
    
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Kullanıcı'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        verbose_name='İşlem Tipi'
    )
    amount = models.IntegerField(verbose_name='Miktar')
    balance_after = models.IntegerField(verbose_name='İşlem Sonrası Bakiye')
    reason = models.CharField(max_length=200, verbose_name='Sebep')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='İşlem Tarihi')
    
    class Meta:
        db_table = 'credit_transactions'
        verbose_name = 'Kredi İşlemi'
        verbose_name_plural = 'Kredi İşlemleri'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_profile', '-created_at']),
        ]
    
    def __str__(self):
        symbol = '+' if self.transaction_type == 'CREDIT' else '-'
        return f"{self.user_profile.user.username} - {symbol}{self.amount} ({self.reason})"


class CommentHistory(models.Model):
    """
    Kullanıcı yorum geçmişi - AI ile yapılan tüm yorumlar
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_history',
        verbose_name='Kullanıcı'
    )
    match_id = models.BigIntegerField(verbose_name='Maç ID', db_index=True)
    match_info = models.CharField(max_length=500, blank=True, verbose_name='Maç Bilgisi')
    user_question = models.TextField(verbose_name='Kullanıcı Sorusu')
    ai_response = models.TextField(verbose_name='AI Cevabı')
    credits_used = models.IntegerField(default=1, verbose_name='Kullanılan Kredi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih', db_index=True)
    
    class Meta:
        db_table = 'comment_history'
        verbose_name = 'Yorum Geçmişi'
        verbose_name_plural = 'Yorum Geçmişleri'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['match_id', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - Maç {self.match_id} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class CreditPurchase(models.Model):
    """
    Özel kredi satın alma siparişleri
    Normal kullanıcı: 1.49 TL - Kullanıcı istediği kadar kredi alabilir
    Supervisor: 0.29 TL - Sadece satış için (maçlarda kullanamaz)
    """
    PAYMENT_STATUS = [
        ('PENDING', 'Beklemede'),
        ('APPROVED', 'Onaylandı'),
        ('REJECTED', 'Reddedildi'),
        ('COMPLETED', 'Tamamlandı'),
    ]
    
    CREDIT_PRICE_NORMAL = 1.49  # TL - Normal kullanıcı fiyatı
    CREDIT_PRICE_SUPERVISOR = 0.29  # TL - Supervisor fiyatı (toptan)
    
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='credit_purchases',
        verbose_name='Kullanıcı'
    )
    credit_amount = models.IntegerField(verbose_name='Kredi Miktarı')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fiyat (TL)')
    payment_code = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,  # unique yerine index
        verbose_name='Ödeme Kodu',
        help_text='Havale/EFT açıklamasına yazılacak benzersiz kod'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING',
        verbose_name='Ödeme Durumu'
    )
    payment_note = models.TextField(blank=True, verbose_name='Ödeme Notu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sipariş Tarihi')
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Onay Tarihi')
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_purchases',
        verbose_name='Onaylayan Admin'
    )
    
    class Meta:
        db_table = 'credit_purchases'
        verbose_name = 'Kredi Siparişi'
        verbose_name_plural = 'Kredi Siparişleri'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_profile', '-created_at']),
            models.Index(fields=['payment_status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.credit_amount} Kredi ({self.price} TL) - {self.get_payment_status_display()}"
    
    @classmethod
    def calculate_price(cls, credit_amount, is_supervisor=False):
        """Kredi miktarına göre fiyat hesapla"""
        price = cls.CREDIT_PRICE_SUPERVISOR if is_supervisor else cls.CREDIT_PRICE_NORMAL
        return credit_amount * price
    
    def generate_payment_code(self):
        """Benzersiz ödeme kodu oluştur: KREDI-[ID]-[USERNAME]"""
        # Kullanıcı adını al (tamamı, en fazla 15 karakter)
        username = self.user_profile.user.username
        # Özel karakterleri temizle (sadece harf ve rakam)
        username_clean = ''.join(c for c in username if c.isalnum())
        # Uppercase yap ve maksimum 15 karakter
        username_part = username_clean[:15].upper()
        # Sipariş ID (5 haneli, başına 0 ekle)
        order_id = str(self.id).zfill(5)
        return f"KREDI-{order_id}-{username_part}"
    
    def save(self, *args, **kwargs):
        """Fiyat ve ödeme kodunu otomatik oluştur"""
        # Fiyatı hesapla (supervisor olup olmadığını kontrol et)
        if not self.price:
            is_supervisor = self.user_profile.is_supervisor
            self.price = self.calculate_price(self.credit_amount, is_supervisor)
        
        # İlk kayıt - ID henüz yok, önce kaydet
        if not self.pk:
            super().save(*args, **kwargs)
            # Şimdi ID var, ödeme kodunu oluştur
            self.payment_code = self.generate_payment_code()
            # Tekrar kaydet (payment_code ile)
            super().save(update_fields=['payment_code'])
        else:
            # Güncelleme - normal kaydet
            super().save(*args, **kwargs)


class SupervisorCreditPurchase(models.Model):
    """
    Supervisor (P2P Satıcı) üzerinden kredi satın alma siparişleri
    Normal kullanıcılar, supervisor'lardan supervisor_price üzerinden kredi alır
    """
    PAYMENT_STATUS = [
        ('PENDING', 'Beklemede'),
        ('APPROVED', 'Onaylandı'),
        ('REJECTED', 'Reddedildi'),
        ('CANCELLED', 'İptal Edildi'),
    ]
    
    buyer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='supervisor_purchases',
        verbose_name='Alıcı Kullanıcı'
    )
    supervisor = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='supervisor_sales',
        verbose_name='Satıcı (Supervisor)',
        limit_choices_to={'is_supervisor': True}
    )
    credit_amount = models.IntegerField(verbose_name='Kredi Miktarı')
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name='Birim Fiyat (TL)',
        help_text='Supervisor\'un belirlediği kredi başına fiyat'
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Toplam Fiyat (TL)'
    )
    payment_code = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
        verbose_name='Ödeme Kodu',
        help_text='Havale/EFT açıklamasına yazılacak kod'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING',
        verbose_name='Ödeme Durumu'
    )
    payment_note = models.TextField(blank=True, verbose_name='Ödeme Notu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sipariş Tarihi')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tamamlanma Tarihi')
    
    # Supervisor onay notu
    supervisor_note = models.TextField(blank=True, verbose_name='Supervisor Notu')
    
    class Meta:
        db_table = 'supervisor_credit_purchases'
        verbose_name = 'Supervisor Kredi Siparişi'
        verbose_name_plural = 'Supervisor Kredi Siparişleri'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['buyer', '-created_at']),
            models.Index(fields=['supervisor', '-created_at']),
            models.Index(fields=['payment_status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.buyer.user.username} → {self.supervisor.user.username} - {self.credit_amount} Kredi ({self.total_price} TL)"
    
    def generate_payment_code(self):
        """Benzersiz ödeme kodu oluştur: P2P-[ID]-[BUYER_USERNAME]"""
        username = self.buyer.user.username
        username_clean = ''.join(c for c in username if c.isalnum())
        username_part = username_clean[:15].upper()
        order_id = str(self.id).zfill(5)
        return f"P2P-{order_id}-{username_part}"
    
    def save(self, *args, **kwargs):
        """Fiyat ve ödeme kodunu otomatik oluştur"""
        # Toplam fiyatı hesapla
        if self.credit_amount and self.unit_price:
            self.total_price = self.credit_amount * self.unit_price
        
        # İlk kayıt
        if not self.pk:
            super().save(*args, **kwargs)
            self.payment_code = self.generate_payment_code()
            super().save(update_fields=['payment_code'])
        else:
            super().save(*args, **kwargs)
    
    def approve_order(self):
        """
        Supervisor siparişi onaylar:
        1. Supervisor kredisi azaltılır
        2. Buyer kredisi artırılır
        3. Sayaçlar güncellenir
        """
        from django.utils import timezone
        
        if self.payment_status != 'PENDING':
            return False, "Sipariş zaten işlenmiş"
        
        # Supervisor'un yeterli kredisi var mı?
        if not self.supervisor.can_sell_credits(self.credit_amount):
            return False, "Supervisor'un yeterli kredisi yok"
        
        # Kredileri transfer et
        self.supervisor.deduct_credits(
            self.credit_amount,
            reason=f'P2P Satış: {self.buyer.user.username}\'e {self.credit_amount} kredi'
        )
        
        self.buyer.add_credits(
            self.credit_amount,
            reason=f'P2P Alım: {self.supervisor.user.username}\'den {self.credit_amount} kredi'
        )
        
        # Sipariş durumunu güncelle
        self.payment_status = 'APPROVED'
        self.completed_at = timezone.now()
        self.save()
        
        # Supervisor sayaçlarını güncelle
        self.supervisor.supervisor_completed_orders += 1
        self.supervisor.save(update_fields=['supervisor_completed_orders'])
        
        return True, "Sipariş başarıyla onaylandı"
    
    def reject_order(self, reason=''):
        """Siparişi reddet"""
        from django.utils import timezone
        
        if self.payment_status != 'PENDING':
            return False, "Sipariş zaten işlenmiş"
        
        self.payment_status = 'REJECTED'
        self.completed_at = timezone.now()
        if reason:
            self.supervisor_note = reason
        self.save()
        
        return True, "Sipariş reddedildi"


class SupervisorApplication(models.Model):
    """
    Supervisor (Satıcı) Başvuruları
    Kullanıcılar satıcı olmak için başvuru yapar, admin onaylar
    """
    APPLICATION_STATUS = [
        ('PENDING', 'Beklemede'),
        ('APPROVED', 'Onaylandı'),
        ('REJECTED', 'Reddedildi'),
    ]
    
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='supervisor_applications',
        verbose_name='Kullanıcı'
    )
    
    # Başvuru Bilgileri
    bank_name = models.CharField(max_length=100, verbose_name='Banka Adı')
    iban = models.CharField(max_length=34, verbose_name='IBAN')
    account_holder = models.CharField(max_length=200, verbose_name='Hesap Sahibi')
    proposed_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.35,
        verbose_name='Önerilen Satış Fiyatı (TL/kredi)',
        help_text='Kredilerinizi kaça satmak istiyorsunuz?'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Açıklama',
        help_text='Neden satıcı olmak istiyorsunuz? (İsteğe bağlı)'
    )
    
    # Durum
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS,
        default='PENDING',
        verbose_name='Başvuru Durumu'
    )
    
    # Tarihler
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Başvuru Tarihi')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='İnceleme Tarihi')
    
    # Admin Bilgileri
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        verbose_name='İnceleyen Admin'
    )
    admin_note = models.TextField(blank=True, verbose_name='Admin Notu')
    
    class Meta:
        db_table = 'supervisor_applications'
        verbose_name = 'Supervisor Başvurusu'
        verbose_name_plural = 'Supervisor Başvuruları'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_profile', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.get_status_display()} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def approve(self, admin_user, note=''):
        """Başvuruyu onayla ve kullanıcıyı supervisor yap"""
        from django.utils import timezone
        
        if self.status != 'PENDING':
            return False, "Başvuru zaten işlenmiş"
        
        # Kullanıcıyı supervisor yap
        profile = self.user_profile
        profile.is_supervisor = True
        profile.supervisor_is_active = True
        profile.supervisor_price = self.proposed_price
        profile.supervisor_bank_name = self.bank_name
        profile.supervisor_iban = self.iban
        profile.supervisor_account_holder = self.account_holder
        profile.save()
        
        # Başvuruyu onayla
        self.status = 'APPROVED'
        self.reviewed_at = timezone.now()
        self.reviewed_by = admin_user
        self.admin_note = note
        self.save()
        
        return True, f"{profile.user.username} başarıyla supervisor olarak onaylandı"
    
    def reject(self, admin_user, note=''):
        """Başvuruyu reddet"""
        from django.utils import timezone
        
        if self.status != 'PENDING':
            return False, "Başvuru zaten işlenmiş"
        
        self.status = 'REJECTED'
        self.reviewed_at = timezone.now()
        self.reviewed_by = admin_user
        self.admin_note = note
        self.save()
        
        return True, "Başvuru reddedildi"


class CreditTransfer(models.Model):
    """Kullanıcılar arası kredi transferi"""
    from_user = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='sent_transfers',
        verbose_name='Gönderen'
    )
    to_user = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='received_transfers',
        verbose_name='Alıcı'
    )
    amount = models.IntegerField(verbose_name='Kredi Miktarı')
    note = models.CharField(max_length=200, blank=True, null=True, verbose_name='Not')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Transfer Tarihi')
    
    class Meta:
        db_table = 'credit_transfers'
        verbose_name = 'Kredi Transferi'
        verbose_name_plural = 'Kredi Transferleri'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['from_user', '-created_at']),
            models.Index(fields=['to_user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.from_user.user.username} → {self.to_user.user.username} ({self.amount} kredi)"
    
    def save(self, *args, **kwargs):
        """Transfer işlemini gerçekleştir"""
        if not self.pk:  # İlk kayıt
            # Gönderenin yeterli kredisi var mı?
            if self.from_user.credits < self.amount:
                raise ValueError("Yetersiz kredi bakiyesi")
            
            # Transfer işlemi
            self.from_user.credits -= self.amount
            self.to_user.credits += self.amount
            
            self.from_user.save()
            self.to_user.save()
        
        super().save(*args, **kwargs)


# ==============================================================================
# 💬 DESTEK SİSTEMİ (SUPPORT TICKETS)
# ==============================================================================

class SupportTicket(models.Model):
    """
    Kullanıcı destek talepleri ve mesajlaşma sistemi
    """
    STATUS_CHOICES = [
        ('OPEN', 'Açık'),
        ('IN_PROGRESS', 'Cevaplanıyor'),
        ('CLOSED', 'Kapatıldı'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Düşük'),
        ('MEDIUM', 'Orta'),
        ('HIGH', 'Yüksek'),
        ('URGENT', 'Acil'),
    ]
    
    CATEGORY_CHOICES = [
        ('GENERAL', 'Genel Soru'),
        ('TECHNICAL', 'Teknik Sorun'),
        ('PAYMENT', 'Ödeme/Kredi'),
        ('SUPERVISOR', 'Supervisor Başvuru'),
        ('FEEDBACK', 'Öneri/Geri Bildirim'),
        ('OTHER', 'Diğer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200, verbose_name='Konu')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GENERAL', verbose_name='Kategori')
    message = models.TextField(verbose_name='Mesaj')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN', verbose_name='Durum')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM', verbose_name='Öncelik')
    
    # Admin cevabı
    admin_response = models.TextField(blank=True, null=True, verbose_name='Admin Cevabı')
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='responded_tickets', verbose_name='Cevaplayan')
    responded_at = models.DateTimeField(null=True, blank=True, verbose_name='Cevaplanma Tarihi')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        db_table = 'support_tickets'
        verbose_name = 'Destek Talebi'
        verbose_name_plural = 'Destek Talepleri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.id} - {self.user.username} - {self.subject}"
    
    def mark_as_responded(self, admin_user, response):
        """Destek talebini cevaplanmış olarak işaretle"""
        self.admin_response = response
        self.responded_by = admin_user
        self.responded_at = timezone.now()
        self.status = 'IN_PROGRESS'
        self.save()
    
    def close(self):
        """Destek talebini kapat"""
        self.status = 'CLOSED'
        self.save()


# ==============================================================================
# 📢 DUYURU SİSTEMİ (ANNOUNCEMENTS)
# ==============================================================================

class Announcement(models.Model):
    """
    Sistem duyuruları - Tüm kullanıcılara gösterilir
    """
    TYPE_CHOICES = [
        ('INFO', 'Bilgi'),
        ('SUCCESS', 'Başarı'),
        ('WARNING', 'Uyarı'),
        ('DANGER', 'Önemli'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Başlık')
    content = models.TextField(verbose_name='İçerik')
    announcement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INFO', verbose_name='Tip')
    
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_pinned = models.BooleanField(default=False, verbose_name='Sabitle (Üstte Göster)')
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Oluşturan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    # Gösterilme tarihleri
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Başlangıç Tarihi')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Bitiş Tarihi')
    
    class Meta:
        db_table = 'announcements'
        verbose_name = 'Duyuru'
        verbose_name_plural = 'Duyurular'
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({'Aktif' if self.is_active else 'Pasif'})"
    
    def is_valid(self):
        """Duyuru şu an gösterilmeli mi?"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class UserAnnouncementRead(models.Model):
    """
    Kullanıcıların okuduğu duyuruları takip eder
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_announcements')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='read_by_users')
    read_at = models.DateTimeField(auto_now_add=True, verbose_name='Okunma Tarihi')
    
    class Meta:
        db_table = 'user_announcement_reads'
        verbose_name = 'Okunmuş Duyuru'
        verbose_name_plural = 'Okunmuş Duyurular'
        unique_together = ['user', 'announcement']
    
    def __str__(self):
        return f"{self.user.username} - {self.announcement.title}"

