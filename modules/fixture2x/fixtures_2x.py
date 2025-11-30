"""
FIXTURES 2X TRANSFORMATION - Team ve Opponent Mantığı
fixtures_results tablosunu 2x yapar: her maçı hem ev sahibi hem deplasman takımı perspektifinden görür
"""

import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import source_db, analytics_db

class Fixtures2x:
    """
    fixtures_results tablosunu 2x transformation ile dönüştürür
    """
    
    def __init__(self):
        self.source_db = source_db
        self.analytics_db = analytics_db
        self.custom_functions = []  # Özel fonksiyonlar listesi
    
    def add_function(self, func, active=True):
        """Özel fonksiyon ekle"""
        self.custom_functions.append({'func': func, 'active': active})
        status = "AKTİF" if active else "PASİF"
        print(f"   ✅ {func.__name__} eklendi ({status})")
    
    def set_function_status(self, func_name, active):
        """Fonksiyon aktif/pasif yap"""
        for item in self.custom_functions:
            if item['func'].__name__ == func_name:
                item['active'] = active
                status = "AKTİF" if active else "PASİF"
                print(f"   🔄 {func_name} -> {status}")
                return
        print(f"   ❌ {func_name} bulunamadı")
    
    def apply_custom_functions(self, df):
        """Aktif fonksiyonları uygula"""
        active_funcs = [item for item in self.custom_functions if item['active']]
        
        if not active_funcs:
            return df
            
        print(f"🔧 {len(active_funcs)} özel fonksiyon uygulanıyor...")
        
        for item in active_funcs:
            func = item['func']
            try:
                df = func(df)
                print(f"   ✅ {func.__name__} tamamlandı")
            except Exception as e:
                print(f"   ❌ {func.__name__} hatası: {e}")
        
        return df
        
    def get_source_data(self):
        """Kaynak veritabanından fixture verilerini çek"""
        print("📊 Kaynak veriler çekiliyor...")
        
        query = "SELECT * FROM fixtures_results"
        
        df = self.source_db.query_df(query)
        
        if df is not None:
            print(f"   ✅ {len(df):,} kayıt çekildi")
        else:
            print("   ❌ Veri çekilemedi")
            
        return df
    
    def transform_2x(self, df):
        """2x transformation uygula: Sadece birebir kopyalama, analiz yok"""
        print("🔄 2x Transformation uygulanıyor...")
        
        if df is None or len(df) == 0:
            print("   ❌ Dönüştürülecek veri yok")
            return None
        
        # 1️⃣ EV SAHİBİ PERSPEKTİFİ - Birebir kopyala
        home_perspective = df.copy()
        home_perspective['team_id'] = home_perspective['home_team_id']
        home_perspective['opponent_team_id'] = home_perspective['away_team_id']
        home_perspective['team_name'] = home_perspective['home_team_name']
        home_perspective['opponent_team_name'] = home_perspective['away_team_name']
        home_perspective['is_home'] = 1
        home_perspective['is_away'] = 0
        home_perspective['team_score'] = home_perspective['home_score']
        home_perspective['opponent_score'] = home_perspective['away_score']
        home_perspective['team_score_1h'] = home_perspective['home_score_1h']
        home_perspective['opponent_score_1h'] = home_perspective['away_score_1h']
        # 2. yarı skoru = Toplam - 1. yarı
        home_perspective['team_score_2h'] = home_perspective['home_score'] - home_perspective['home_score_1h']
        home_perspective['opponent_score_2h'] = home_perspective['away_score'] - home_perspective['away_score_1h']
        
        # 2️⃣ DEPLASMAN PERSPEKTİFİ - Birebir kopyala 
        away_perspective = df.copy()
        away_perspective['team_id'] = away_perspective['away_team_id']
        away_perspective['opponent_team_id'] = away_perspective['home_team_id']
        away_perspective['team_name'] = away_perspective['away_team_name']
        away_perspective['opponent_team_name'] = away_perspective['home_team_name']
        away_perspective['is_home'] = 0
        away_perspective['is_away'] = 1
        away_perspective['team_score'] = away_perspective['away_score']
        away_perspective['opponent_score'] = away_perspective['home_score']
        away_perspective['team_score_1h'] = away_perspective['away_score_1h']
        away_perspective['opponent_score_1h'] = away_perspective['home_score_1h']
        # 2. yarı skoru = Toplam - 1. yarı
        away_perspective['team_score_2h'] = away_perspective['away_score'] - away_perspective['away_score_1h']
        away_perspective['opponent_score_2h'] = away_perspective['home_score'] - away_perspective['home_score_1h']
        
        # 3️⃣ BİRLEŞTİR
        transformed_df = pd.concat([home_perspective, away_perspective], ignore_index=True)
        
        # 3.5️⃣ ÖZEL FONKSİYONLARI UYGULA
        transformed_df = self.apply_custom_functions(transformed_df)
        
        # 3.6️⃣ ZAMAN DAMGALARI EKLE
        try:
            from .timestamp_utils import add_timestamps
        except ImportError:
            from timestamp_utils import add_timestamps
        transformed_df = add_timestamps(transformed_df)
        
        # 4️⃣ GEREKSİZ SÜTUNLARI ÇIKAR
        columns_to_remove = [
            'home_team_id', 'away_team_id', 
            'home_team_name', 'away_team_name',
            'home_score', 'away_score', 
            'home_score_1h', 'away_score_1h'
        ]
        
        # Hangi kolonlar mevcut
        print(f"   📋 Transformation öncesi kolon sayısı: {len(transformed_df.columns)}")
        existing_columns_to_remove = [col for col in columns_to_remove if col in transformed_df.columns]
        print(f"   🗑️ Silinecek kolonlar: {existing_columns_to_remove}")
        
        transformed_df.drop(columns=existing_columns_to_remove, inplace=True)
        print(f"   📋 Transformation sonrası kolon sayısı: {len(transformed_df.columns)}")
        
        return transformed_df
    
    def save_to_analytics(self, df, table_name="fixtures_2x"):
        """Analytics veritabanına kaydet"""
        if df is None or len(df) == 0:
            print("   ❌ Kaydedilecek veri yok")
            return False
            
        print(f"💾 Analytics DB'ye kaydediliyor ({table_name})...")
        
        success = self.analytics_db.bulk_df(df, table_name, replace=True)
        
        if success:
            print(f"   ✅ {len(df):,} kayıt başarıyla kaydedildi")
        else:
            print("   ❌ Kaydetme başarısız")
            
        return success
    
    def run_full_transformation(self, table_name="fixtures_2x"):
        """Tam transformation süreci"""
        print("🚀 FIXTURES 2X TRANSFORMATION BAŞLIYOR")
        print("="*60)
        
        # 1. Veriyi çek
        source_data = self.get_source_data()
        if source_data is None:
            return False
        
        # 2. 2x transformation uygula
        transformed_data = self.transform_2x(source_data)
        if transformed_data is None:
            return False
        
        # 3. Analytics DB'ye kaydet
        success = self.save_to_analytics(transformed_data, table_name)
        
        if success:
            print(f"\n🎉 TRANSFORMATION TAMAMLANDI!")
            print(f"   📊 Kaynak: {len(source_data):,} maç")
            print(f"   🔄 Sonuç: {len(transformed_data):,} kayıt")
            print(f"   💾 Tablo: {table_name}")
        
        return success


def run_fixtures_2x_transformation():
    """Basit kullanım fonksiyonu"""
    transformer = Fixtures2x()
    return transformer.run_full_transformation()


if __name__ == "__main__":
    run_fixtures_2x_transformation()