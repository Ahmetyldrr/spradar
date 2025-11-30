"""
🔧 Service Logger - Cron servisleri için log yazdırma helper
"""

import os
import sys
import django
from datetime import datetime
from typing import Optional, Dict, Any

# Django setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spradar_api.settings')
django.setup()

from django.utils import timezone
from api.models import CronService, ServiceLog


class ServiceLogger:
    """
    Servis logları için helper class
    
    Kullanım:
        logger = ServiceLogger('FIXTURE2X')
        logger.start('Fixture 2X İşlemi Başladı')
        # ... işlemler ...
        logger.success('İşlem tamamlandı', processed=100, duration=45.2)
    """
    
    def __init__(self, service_name: str):
        """
        Args:
            service_name: CronService.name değeri (örn: 'Fixture 2X', 'Commentary', 'Comeback')
        """
        self.service_name = service_name
        self.service = None
        self.start_time = None
        
        # Servisi bul veya oluştur
        self._get_or_create_service()
    
    def _get_or_create_service(self):
        """Servisi bul, yoksa oluştur"""
        try:
            from api.models import CronService
            self.service, created = CronService.objects.get_or_create(
                name=self.service_name,
                defaults={
                    'service_type': self._guess_service_type(),
                    'is_active': True
                }
            )
            if created:
                print(f"✅ Yeni servis oluşturuldu: {self.service_name}")
        except Exception as e:
            print(f"⚠️  Servis oluşturulamadı: {e}")
            self.service = None
    
    def _guess_service_type(self) -> str:
        """Servis adından tipi tahmin et"""
        name_lower = self.service_name.lower()
        if 'fixture' in name_lower or '2x' in name_lower:
            return 'FIXTURE2X'
        elif 'commentary' in name_lower:
            return 'COMMENTARY'
        elif 'comeback' in name_lower:
            return 'COMEBACK'
        elif 'srservice' in name_lower or 'sr_service' in name_lower:
            return 'SRSERVICE'
        else:
            return 'OTHER'
    
    def start(self, operation_name: str):
        """İşlem başladığında çağrılır"""
        self.start_time = timezone.now()
        self.log(
            operation_name=operation_name,
            status='INFO',
            message='İşlem başladı'
        )
    
    def success(
        self,
        operation_name: str,
        message: str = '',
        processed: Optional[int] = None,
        errors: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """İşlem başarılı olduğunda çağrılır"""
        duration = None
        if self.start_time:
            duration = (timezone.now() - self.start_time).total_seconds()
        
        self.log(
            operation_name=operation_name,
            status='SUCCESS',
            message=message or 'İşlem başarıyla tamamlandı',
            duration=duration,
            processed=processed,
            errors=errors,
            details=details
        )
        
        # Servis son durumunu güncelle
        if self.service:
            self.service.last_run = timezone.now()
            self.service.last_status = True
            self.service.save()
    
    def error(
        self,
        operation_name: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """İşlem hata verdiğinde çağrılır"""
        duration = None
        if self.start_time:
            duration = (timezone.now() - self.start_time).total_seconds()
        
        self.log(
            operation_name=operation_name,
            status='ERROR',
            message=message,
            duration=duration,
            details=details
        )
        
        # Servis son durumunu güncelle
        if self.service:
            self.service.last_run = timezone.now()
            self.service.last_status = False
            self.service.save()
    
    def warning(
        self,
        operation_name: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Uyarı logları için"""
        self.log(
            operation_name=operation_name,
            status='WARNING',
            message=message,
            details=details
        )
    
    def info(
        self,
        operation_name: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Bilgi logları için"""
        self.log(
            operation_name=operation_name,
            status='INFO',
            message=message,
            details=details
        )
    
    def log(
        self,
        operation_name: str,
        status: str,
        message: str = '',
        duration: Optional[float] = None,
        processed: Optional[int] = None,
        errors: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Genel log fonksiyonu"""
        if not self.service:
            print(f"⚠️  Servis bulunamadı, log kaydedilemedi: {operation_name}")
            return
        
        try:
            from api.models import ServiceLog
            ServiceLog.objects.create(
                service=self.service,
                operation_name=operation_name,
                status=status,
                message=message,
                duration_seconds=duration,
                processed_count=processed,
                error_count=errors,
                details=details
            )
        except Exception as e:
            print(f"⚠️  Log kaydedilemedi: {e}")


# Kolay kullanım için factory fonksiyonlar
def get_logger(service_name: str) -> ServiceLogger:
    """
    ServiceLogger instance'ı döndürür
    
    Örnek:
        from api.service_logger import get_logger
        logger = get_logger('Fixture 2X')
        logger.success('İşlem tamamlandı', processed=100)
    """
    return ServiceLogger(service_name)


def log_service_run(
    service_name: str,
    operation_name: str,
    status: str,
    message: str = '',
    **kwargs
):
    """
    Tek satırda log yazmak için
    
    Örnek:
        from api.service_logger import log_service_run
        log_service_run('Fixture 2X', 'Günlük İşlem', 'SUCCESS', processed=100)
    """
    logger = ServiceLogger(service_name)
    logger.log(
        operation_name=operation_name,
        status=status,
        message=message,
        **kwargs
    )
