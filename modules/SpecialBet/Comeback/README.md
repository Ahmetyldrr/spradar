# 🔄 Comeback Analysis Module

Takımların **ilk yarı - maç sonu** farklı sonuçlarını analiz eden modül.

## 📊 Ne Yapar?

Belirli bir tarihteki tüm maçlar için:
1. **source_db**'den maçları çeker (`current_week_fixtures`)
2. Her takımın **sezon içi tüm maçlarını** analiz eder (`fixtures_results`)
3. **9 farklı HT-FT senaryosunu** hesaplar
4. İstatistikleri **sr_analiz_db**'ye kaydeder

## 🎯 Comeback Senaryoları

| Kod | Açıklama | Önem |
|-----|----------|------|
| **HT2FT1** | İlk yarı geride → Maç sonu kazandı | ⭐⭐⭐ ASIL COMEBACK! |
| **HT2FT0** | İlk yarı geride → Maç sonu berabere | ⭐⭐ Kurtardı |
| **HT1FT2** | İlk yarı önde → Maç sonu kaybetti | 🚨 Rezalet |
| **HT1FT0** | İlk yarı önde → Maç sonu berabere | ⚠️ Puan kaybı |
| **HT0FT1** | İlk yarı berabere → Maç sonu kazandı | ✅ İyi son |
| **HT0FT2** | İlk yarı berabere → Maç sonu kaybetti | ❌ Kötü son |
| **HT1FT1** | İlk yarı önde → Maç sonu da önde | ✅ Stabil |
| **HT2FT2** | İlk yarı geride → Maç sonu da geride | ❌ Stabil kayıp |
| **HT0FT0** | İlk yarı berabere → Maç sonu berabere | ⚪ Sıkıcı |

## 🗂️ Veritabanı Yapısı

**Tablo: `comeback_analysis`** (sr_analiz_db)

### Maç Bilgileri
- `match_id`, `season_id`, `match_date`, `match_time`
- `home_team_id`, `home_team_name`
- `away_team_id`, `away_team_name`
- `country`, `league`, `round`, `week`

### Ev Sahibi İstatistikleri
- `home_total_matches` - Toplam maç sayısı
- `home_ht1ft2_count`, `home_ht1ft2_pct` - İlk yarı önde → Maç kaybetti (sayı + %)
- `home_ht1ft0_count`, `home_ht1ft0_pct` - İlk yarı önde → Berabere (sayı + %)
- `home_ht0ft1_count`, `home_ht0ft1_pct` - Beraberden kazandı (sayı + %)
- `home_ht2ft1_count`, `home_ht2ft1_pct` - **COMEBACK!** Geriden kazandı (sayı + %)
- `home_ht2ft0_count`, `home_ht2ft0_pct` - Geriden berabere (sayı + %)
- `home_ht0ft2_count`, `home_ht0ft2_pct` - Beraberden kaybetti (sayı + %)
- `home_ht1ft1_count`, `home_ht1ft1_pct` - Önde başlayıp kazandı (sayı + %)
- `home_ht2ft2_count`, `home_ht2ft2_pct` - Geride başlayıp kaybetti (sayı + %)
- `home_ht0ft0_count`, `home_ht0ft0_pct` - Berabere başlayıp berabere (sayı + %)

### Deplasman İstatistikleri
(Aynı sütunlar `away_` prefix'i ile)

### Metadata
- `created_at` - Kayıt zamanı

## 🚀 Kullanım

### 1. Komut satırı ile
```bash
cd /home/ahmet/Desktop/Spradar1
source .venv/bin/activate
python modules/SpecialBet/Comeback/comeback_main.py 06/11/25
```

### 2. İnteraktif
```bash
python modules/SpecialBet/Comeback/comeback_main.py
# Tarih soracak, girersiniz
```

## 📈 Örnek Çıktı

```
================================================================================
🔄 COMEBACK ANALYSIS SYSTEM
================================================================================
📅 İşlenecek Tarih: 06/11/25
⏰ İşlem Zamanı: 2025-11-06 15:30:00
================================================================================

🔌 Veritabanı bağlantıları kuruluyor...
✅ Bağlantılar başarılı!

📊 06/11/25 tarihindeki maçlar yükleniyor...
✅ 53 maç bulundu!

================================================================================
🔄 Comeback analizleri yapılıyor...
================================================================================

📊 Maç 1/53: Manchester United vs Chelsea
   ✅ Analiz tamamlandı
📊 Maç 2/53: Real Madrid vs Barcelona
   ✅ Analiz tamamlandı
...

✅ Toplam 53 maç analiz edildi!

💾 Veriler sr_analiz_db'ye kaydediliyor...
✅ comeback_analysis tablosuna 53 kayıt eklendi!

================================================================================
✅ İŞLEM TAMAMLANDI!
================================================================================
📊 İşlenen Maç Sayısı: 53
💾 Veritabanı Tablosu: comeback_analysis
📅 Tarih: 06/11/25
⏰ Tamamlanma: 15:31:45
================================================================================
```

## 🔍 Örnek Sorgular

### En çok comeback yapan takımlar
```sql
SELECT 
    home_team_name,
    home_total_matches,
    home_ht2ft1_count as comeback_sayisi,
    home_ht2ft1_pct as comeback_yuzdesi
FROM comeback_analysis
WHERE home_ht2ft1_pct > 0
ORDER BY home_ht2ft1_pct DESC
LIMIT 10;
```

### Bugünkü maçlarda comeback potansiyeli
```sql
SELECT 
    match_date,
    match_time,
    home_team_name,
    away_team_name,
    home_ht2ft1_pct as ev_comeback_pct,
    away_ht2ft1_pct as dep_comeback_pct
FROM comeback_analysis
WHERE match_date = '06/11/25'
AND (home_ht2ft1_pct > 15 OR away_ht2ft1_pct > 15)
ORDER BY (home_ht2ft1_pct + away_ht2ft1_pct) DESC;
```

### İlk yarıda önde olup maç kaybeden takımlar (rezalet)
```sql
SELECT 
    home_team_name,
    home_ht1ft2_count as rezalet_sayisi,
    home_ht1ft2_pct as rezalet_yuzdesi,
    home_total_matches
FROM comeback_analysis
WHERE home_ht1ft2_pct > 20
ORDER BY home_ht1ft2_pct DESC;
```

## 📦 Modül Yapısı

```
Comeback/
├── __init__.py              # Modül tanıtımı
├── comeback_analyzer.py     # ComebackAnalyzer sınıfı
├── comeback_main.py         # Ana işleyici
└── README.md               # Bu dosya
```

## 🔧 Teknik Detaylar

### Veri Kaynağı
- **source_db** (sport_db)
  - `current_week_fixtures` - Günün maçları
  - `fixtures_results` - Geçmiş maç sonuçları

### Veri Hedefi
- **sr_analiz_db**
  - `comeback_analysis` - Comeback istatistikleri

### İstatistik Hesaplama
1. Takımın sezon içi **TÜM** maçları çekilir
2. Her maç için HT-FT senaryosu belirlenir
3. Her senaryonun sayısı ve yüzdesi hesaplanır
4. Ev sahibi ve deplasman ayrı ayrı analiz edilir

## 📊 Kullanım Senaryoları

1. **Comeback Avcıları**: HT2FT1 oranı yüksek takımları bulun
2. **Güvenli İlk Yarı**: HT1FT1 oranı yüksek takımları bulun
3. **Risk Analizi**: HT1FT2 oranı yüksek takımlardan kaçının
4. **Berabere Uzmanları**: HT0FT0 oranı yüksek takımları bulun

## 🎯 Sonraki Adımlar

- [ ] AI ile comeback tahmini
- [ ] Grafiksel raporlama
- [ ] Tarih aralığı desteği
- [ ] Lig bazlı analiz

---

**Version:** 1.0.0  
**Author:** Spradar Analytics Team  
**Date:** November 6, 2025
