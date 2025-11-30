"""
TIMESTAMP UTILITY - Zaman Damgası Yardımcı Fonksiyonları
======================================================
bulk_df yapılan her dosyaya timestamp ekleme utilityleri
"""

from datetime import datetime
import pandas as pd


def add_timestamps(df):
    """
    DataFrame'e created_at ve updated_at zaman damgaları ekle
    
    Args:
        df: Pandas DataFrame
        
    Returns:
        DataFrame: Zaman damgaları eklenmiş DataFrame
    """
    if df is None or len(df) == 0:
        return df
        
    df = df.copy()
    current_time = datetime.now()
    
    # Eğer created_at yoksa ekle, varsa güncelleme
    if 'created_at' not in df.columns:
        df['created_at'] = current_time
        print(f"   ⏰ created_at eklendi: {current_time}")
    else:
        print(f"   ℹ️ created_at mevcut, korunuyor")
    
    # Her zaman updated_at güncelle
    df['updated_at'] = current_time  
    print(f"   🔄 updated_at güncellendi: {current_time}")
    
    return df


def add_timestamps_to_bulk_operation(func):
    """
    Decorator: bulk_df operasyonlarına otomatik timestamp ekle
    
    Usage:
        @add_timestamps_to_bulk_operation
        def my_transformation_function(df):
            # transformation logic
            return df
    """
    def wrapper(df, *args, **kwargs):
        # Orijinal fonksiyonu çalıştır
        result_df = func(df, *args, **kwargs)
        
        # Sonuca timestamp ekle
        if result_df is not None:
            result_df = add_timestamps(result_df)
        
        return result_df
    
    return wrapper


def get_timestamp_columns_for_db():
    """
    Veritabanı tablo oluşturma için timestamp kolonlarını döndür
    
    Returns:
        dict: Kolon adı -> Veri tipi mapping'i
    """
    return {
        'created_at': 'TIMESTAMP',
        'updated_at': 'TIMESTAMP'
    }


def format_timestamp_for_db(timestamp):
    """
    Timestamp'i veritabanı formatına çevir
    
    Args:
        timestamp: datetime objesi
        
    Returns:
        str: Veritabanı formatında timestamp string
    """
    if timestamp is None:
        return None
    
    if isinstance(timestamp, str):
        return timestamp
    
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')