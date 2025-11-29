"""
TEAM STATS SYSTEM - Takım İstatistiklerini Hesaplama Sistemi
============================================================
fixtures_2x tablosundan team bazlı istatistikler oluşturur
"""

import pandas as pd
import sys
import os

# Database için path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import analytics_db


class TeamStatsSystem:
    """
    Team bazlı istatistik hesaplama sistemi
    """
    
    def __init__(self):
        self.analytics_db = analytics_db
        self.stats_functions = []
    
    def add_stats_function(self, func, n_matches=5, active=True):
        """İstatistik fonksiyonu ekle"""
        self.stats_functions.append({
            'func': func, 
            'n_matches': n_matches, 
            'active': active
        })
        status = "AKTİF" if active else "PASİF"
        print(f"   ✅ {func.__name__} eklendi ({status}, son {n_matches} maç)")
    
    def set_stats_function_status(self, func_name, active):
        """İstatistik fonksiyon aktif/pasif yap"""
        for item in self.stats_functions:
            if item['func'].__name__ == func_name:
                item['active'] = active
                status = "AKTİF" if active else "PASİF"
                print(f"   🔄 {func_name} -> {status}")
                return
        print(f"   ❌ {func_name} bulunamadı")
    
    def get_fixtures_2x_data(self, source_table="fixtures_2x"):
        """fixtures_2x tablosundan veriyi çek"""
        print(f"📊 {source_table} tablosundan veriler çekiliyor...")
        
        query = f"SELECT * FROM {source_table} ORDER BY match_date DESC"
        df = self.analytics_db.query_df(query)
        
        if df is not None:
            print(f"   ✅ {len(df):,} kayıt çekildi")
        else:
            print("   ❌ Veri çekilemedi")
            
        return df
    
    def calculate_team_stats(self, df):
        """Aktif istatistik fonksiyonlarını çalıştır"""
        active_functions = [item for item in self.stats_functions if item['active']]
        
        if not active_functions:
            print("   ℹ️ Aktif istatistik fonksiyonu yok")
            return None
            
        print(f"📊 {len(active_functions)} istatistik fonksiyonu hesaplanıyor...")
        
        all_stats = []
        
        for item in active_functions:
            func = item['func']
            n_matches = item['n_matches']
            
            try:
                print(f"   🔄 {func.__name__} hesaplanıyor (son {n_matches} maç)...")
                stats_df = func(df, n_matches)
                
                if stats_df is not None and len(stats_df) > 0:
                    # Fonksiyon adını prefix olarak ekle
                    func_prefix = func.__name__.replace('calculate_', '').replace('_stats', '')
                    stats_df.columns = [f'{func_prefix}_{col}' if col not in ['team_id', 'team_name'] 
                                      else col for col in stats_df.columns]
                    all_stats.append(stats_df)
                    print(f"   ✅ {func.__name__} tamamlandı ({len(stats_df)} takım)")
                else:
                    print(f"   ⚠️ {func.__name__} boş sonuç döndü")
                    
            except Exception as e:
                print(f"   ❌ {func.__name__} hatası: {e}")
        
        if not all_stats:
            return None
        
        # Tüm istatistikleri birleştir
        print("🔗 İstatistikler birleştiriliyor...")
        combined_stats = all_stats[0]
        
        for stats_df in all_stats[1:]:
            combined_stats = pd.merge(combined_stats, stats_df, 
                                    on=['team_id', 'team_name'], how='outer')
        
        # Zaman damgası ekle
        try:
            from .timestamp_utils import add_timestamps
        except ImportError:
            from timestamp_utils import add_timestamps
        combined_stats = add_timestamps(combined_stats)
        
        print(f"   ✅ {len(combined_stats)} takım istatistiği hazır")
        return combined_stats
    
    def save_team_stats(self, stats_df, table_name):
        """Takım istatistiklerini analytics DB'ye kaydet"""
        if stats_df is None or len(stats_df) == 0:
            print("   ❌ Kaydedilecek istatistik yok")
            return False
            
        print(f"💾 {table_name} tablosuna kaydediliyor...")
        
        success = self.analytics_db.bulk_df(stats_df, table_name, replace=True)
        
        if success:
            print(f"   ✅ {len(stats_df):,} takım istatistiği kaydedildi")
        else:
            print("   ❌ Kaydetme başarısız")
            
        return success
    
    def run_team_stats_calculation(self, source_table="fixtures_2x", target_table="team_stats", n_matches_override=None):
        """Tam takım istatistik hesaplama süreci"""
        print("🏆 TEAM STATS CALCULATION BAŞLIYOR")
        print("="*60)
        
        # 1. fixtures_2x verisini çek
        fixtures_data = self.get_fixtures_2x_data(source_table)
        if fixtures_data is None:
            return False
        
        # 2. n_matches override varsa uygula
        if n_matches_override:
            for item in self.stats_functions:
                if item['active']:
                    item['n_matches'] = n_matches_override
                    print(f"   🔄 {item['func'].__name__} -> {n_matches_override} maç")
        
        # 3. İstatistikleri hesapla
        team_stats = self.calculate_team_stats(fixtures_data)
        if team_stats is None:
            return False
        
        # 4. Analytics DB'ye kaydet
        success = self.save_team_stats(team_stats, target_table)
        
        if success:
            print(f"\n🎉 TEAM STATS TAMAMLANDI!")
            print(f"   📊 Kaynak: {source_table}")
            print(f"   🏆 Hedef: {target_table}")
            print(f"   📈 Takım Sayısı: {len(team_stats)}")
            print(f"   📋 Kolon Sayısı: {len(team_stats.columns)}")
        
        return success