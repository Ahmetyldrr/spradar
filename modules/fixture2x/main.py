"""
MAIN SCRIPT - Sadece Burada Çalış!
==================================
Fonksiyon ekle/çıkar, aktif/pasif yap, çalıştır!
"""

import sys
import os
from datetime import datetime
import traceback

# Database için path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Aynı klasörden import et
from fixtures_2x import Fixtures2x
from my_functions import add_all_advanced_stats, add_fulltime_over_under, add_ht2_over_under, add_ht_kg, add_match_result_kg, add_result, add_goals, ht2_gol_analiz, ht_gol_analiz, kesin_gol_sayısı, match_gol_analiz
from my_functions import add_ht_over_under

# Team Stats sistemi
from team_stats_system import TeamStatsSystem
from team_stats_functions import calculate_sum_all_stats, calculate_sum_home_stats, calculate_sum_away_stats, calculate_dynamic_streaks, calculate_dynamic_streaks_home, calculate_dynamic_streaks_away

# Log dosyası ayarı
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "fixture2x_cron.log")

def log_message(message, level="INFO"):
    """Log mesajı yaz"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Console'a da yazdır
    print(log_entry.strip())
    
    # Log dosyasına yaz
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(log_entry)

def main():
    """SADECE BURADA EKLEME/ÇIKARMA YAP!"""
    
    start_time = datetime.now()
    log_message("="*60)
    log_message("🚀 FIXTURE 2X SİSTEMİ BAŞLADI")
    log_message("="*60)
    
    try:
        # Sistem oluştur
        log_message("📋 Fixtures 2X sistemi oluşturuluyor...")
        system = Fixtures2x()
        
        # ======================================
        # FONKSİYONLARI EKLE - True/False ile aktif/pasif
        # ======================================
        
        log_message("⚙️  Fonksiyonlar ekleniyor...")
        system.add_function(add_result, True)
        system.add_function(add_goals, True)
        system.add_function(add_ht_over_under, True)
        system.add_function(add_ht2_over_under, True)
        system.add_function(add_fulltime_over_under, True)
        system.add_function(add_ht_kg, True)
        system.add_function(add_match_result_kg, True)
        system.add_function(kesin_gol_sayısı, True)
        system.add_function(ht_gol_analiz, True)
        system.add_function(ht2_gol_analiz, True)
        system.add_function(match_gol_analiz, True)
        system.add_function(add_all_advanced_stats, True)

        # ======================================
        # FIXTURE 2X ÇALIŞTIR!
        # ======================================
        
        log_message("🔄 Fixture 2X transformasyonu başlatılıyor...")
        success = system.run_full_transformation(table_name="fixtures_2x")
        
        if success:
            log_message("✅ Fixture 2x işlem başarılı!", "SUCCESS")
        else:
            log_message("❌ Fixture 2x işlem başarısız!", "ERROR")
            return
        
        # ======================================
        # TEAM STATS SİSTEMİ - SADECE SUM TABLOSU!
        # ======================================
        
        log_message("="*60)
        log_message("🏆 TEAM STATS SİSTEMİ BAŞLIYOR - SADECE SUM TABLOSU!")
        log_message("="*60)
        
        # 1️⃣ TÜM MAÇLAR - Son 10 maç
        log_message("📊 TÜM MAÇLAR - team_sum_last_10 hesaplanıyor...")
        team_system = TeamStatsSystem()
        team_system.add_stats_function(calculate_sum_all_stats, n_matches=5, active=True)
        team_system.run_team_stats_calculation(
            source_table="fixtures_2x", 
            target_table="team_sum_last_10",  # 🎯 Tüm maçlar
            n_matches_override=10
        )


        # 4️⃣ EV SAHİBİ MAÇLARI - Son 10 maç
        log_message("🏠 EV SAHİBİ - team_sum_home_last_10 hesaplanıyor...")
        team_system = TeamStatsSystem()
        team_system.add_stats_function(calculate_sum_home_stats, n_matches=10, active=False)
        team_system.run_team_stats_calculation(
            source_table="fixtures_2x", 
            target_table="team_sum_home_last_10",  # 🎯 Ev sahibi
            n_matches_override=10
        )


        # 6️⃣ DEPLASMAN MAÇLARI - Son 10 maç
        log_message("✈️  DEPLASMAN - team_sum_away_last_10 hesaplanıyor...")
        team_system = TeamStatsSystem()
        team_system.add_stats_function(calculate_sum_away_stats, n_matches=10, active=False)
        team_system.run_team_stats_calculation(
            source_table="fixtures_2x", 
            target_table="team_sum_away_last_10",  # ✈️ Deplasman
            n_matches_override=10
        )

        # 🔥 YENİ! DİNAMİK STREAK HESAPLAMASI - Her özellik için streak!
        log_message("="*60)
        log_message("🔥 DİNAMİK STREAK SİSTEMİ BAŞLIYOR!")
        log_message("="*60)
    
        # 🔥 TÜM MAÇLAR - Streak (SINIRSIZ)
        log_message("🔥 TÜM MAÇLAR - team_dynamic_streaks_all hesaplanıyor...")
        team_system = TeamStatsSystem()
        team_system.add_stats_function(calculate_dynamic_streaks, n_matches=999, active=False)
        team_system.run_team_stats_calculation(
            source_table="fixtures_2x", 
            target_table="team_dynamic_streaks_all",  # 🔥 Tüm maçlar streak
        )

        # 🏠 EV SAHİBİ STREAK - (SINIRSIZ)
        log_message("🏠 EV SAHİBİ STREAK - team_dynamic_streaks_home_all hesaplanıyor...")
        team_system = TeamStatsSystem()
        team_system.add_stats_function(calculate_dynamic_streaks_home, n_matches=999, active=False)
        team_system.run_team_stats_calculation(
            source_table="fixtures_2x", 
            target_table="team_dynamic_streaks_home_all",  # 🏠 Ev sahibi streak
        )

        # ✈️ DEPLASMAN STREAK - (SINIRSIZ)
        log_message("✈️  DEPLASMAN STREAK - team_dynamic_streaks_away_all hesaplanıyor...")
        team_system = TeamStatsSystem()
        team_system.add_stats_function(calculate_dynamic_streaks_away, n_matches=999, active=False)
        team_system.run_team_stats_calculation(
            source_table="fixtures_2x", 
            target_table="team_dynamic_streaks_away_all",  # ✈️ Deplasman streak
        )

        # Başarı
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_message("="*60)
        log_message(f"✅ TÜM İŞLEMLER TAMAMLANDI! (Süre: {duration:.2f} saniye)", "SUCCESS")
        log_message("="*60)
        
    except Exception as e:
        log_message("="*60, "ERROR")
        log_message(f"❌ HATA OLUŞTU: {str(e)}", "ERROR")
        log_message("="*60, "ERROR")
        log_message("Detaylı hata bilgisi:", "ERROR")
        log_message(traceback.format_exc(), "ERROR")
        raise

if __name__ == "__main__":
    main()