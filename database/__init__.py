"""
DATABASE PACKAGE - Modüler Veritabanı Bağlantıları
Tüm projelerde kullanılabilir modüler database yapısı
"""

from .source_connection import SourceConnection
from .analytics_connection import AnalyticsConnection

# Global instances - Direk import edilebilir
source_db = SourceConnection()
analytics_db = AnalyticsConnection()

__all__ = [
    'SourceConnection',
    'AnalyticsConnection',
    'source_db',
    'analytics_db'
]