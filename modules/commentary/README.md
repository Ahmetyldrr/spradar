# 🎯 SPRADAR COMMENTARY SYSTEM v2.1

## Günlük Maç Yorumu Otomatik Oluşturma Sistemi

286 sütunlu `team_sum_last_10` tablosunu kullanarak, **günlük maçlar için otomatik yorum** oluşturan gelişmiş AI RAG sistemi.

---

## 🚀 Yeni Özellikler (v2.1)

### ✨ Günlük Maç İşleme
- `current_week_fixtures` tablosundan **otomatik maç çekme**
- Kullanıcı sadece **tarihi girer**, sistem tüm maçları işler
- Her maç için **kapsamlı yorum** oluşturma

### 💾 JSON Veritabanı Desteği
- Maç bilgileri + yorumlar **JSON sütununda** saklanır
- `daily_match_commentaries` tablosunda merkezi yönetim
- Hızlı arama ve sorgulama

### 📊 Detaylı Maç Bilgileri
- Ülke, lig, sezon, hafta bilgileri
- Ev sahibi/deplasman takım yorumları
- Maç zamanı, stadyum, timezone bilgileri

---

## 📁 Modül Yapısı

```
modules/commentary/
├── __init__.py                  # Modül tanımlamaları
├── team_commentary.py           # 286 sütun takım yorumu
├── match_analysis.py            # İki takım karşılaştırma
├── advanced_stats.py            # Gelişmiş istatistik analizi
├── output_formatter.py          # Çıktı formatları (JSON, MD, TXT)
├── daily_matches.py             # ⭐ Günlük maç işleme
├── daily_commentary.py          # ⭐ Ana kullanım scripti
└── commentary_main.py           # Tek takım/maç analizi scripti
```

---

## 🎯 Kullanım

### 1. Bugünün Maçlarını İşle

```bash
python modules/commentary/daily_commentary.py
```

**Ne Yapar:**
- Bugünün tüm maçlarını çeker
- Her maç için yorum oluşturur
- Veritabanına JSON olarak kaydeder

---

### 2. Belirli Bir Günün Maçlarını İşle

```bash
python modules/commentary/daily_commentary.py --date 05/11/25
```

---

### 3. Günün Maçlarını Listele (İşlemeden)

```bash
python modules/commentary/daily_commentary.py --list
python modules/commentary/daily_commentary.py --list --date 05/11/25
```

**Çıktı Örneği:**
```
📅 05/11/25 MAÇLARI
================================================================================

🏆 Türkiye - Süper Lig (5 maç)
--------------------------------------------------------------------------------
 19:00 | Fenerbahçe                     vs Galatasaray                    
 16:30 | Beşiktaş                       vs Trabzonspor                    

🏆 İngiltere - Premier League (10 maç)
--------------------------------------------------------------------------------
 15:00 | Manchester United              vs Liverpool                      
 17:30 | Arsenal                        vs Chelsea                        
```

---

### 4. Belirli Bir Maçı Görüntüle

```bash
python modules/commentary/daily_commentary.py --match-id 63637731
```

**JSON Çıktısı:**
```json
{
  "match_info": {
    "match_id": 63637731,
    "match_date": "05/11/25",
    "match_time": "13:00",
    "country": "Azerbaycan",
    "league": "Birinci Lig",
    "description": "Azerbaycan - Birinci Lig liginde Baku Sporting (ev sahibi) ile Cabrayil (deplasman) karşılaşacak."
  },
  "home_team": {
    "team_id": 1080914,
    "team_name": "Baku Sporting",
    "commentary": "Ben Baku Sporting takımıyım ve 1080914 numaralı takım ID'sine sahibim. ..."
  },
  "away_team": {
    "team_id": 1080920,
    "team_name": "Cabrayil",
    "commentary": "Ben Cabrayil takımıyım ve 1080920 numaralı takım ID'sine sahibim. ..."
  }
}
```

---

### 5. Tarihe Göre Yorumları Ara

```bash
python modules/commentary/daily_commentary.py --search-date 05/11/25
```

---

### 6. Takıma Göre Yorumları Ara

```bash
python modules/commentary/daily_commentary.py --search-team 3052
```

---

### 7. İnteraktif Mod

```bash
python modules/commentary/daily_commentary.py --interactive
```

**Menü:**
```
🎯 DAILY MATCH COMMENTARY - İnteraktif Mod
================================================================================

📋 İŞLEM SEÇİMİ:
1. Bugünün maçlarını işle ve yorum oluştur
2. Belirli bir günün maçlarını işle
3. Günün maçlarını listele (sadece)
4. Belirli bir maçı görüntüle (Match ID)
5. Tarihe göre yorumları ara
6. Takıma göre yorumları ara
7. Çıkış
```

---

## 💾 Veritabanı Yapısı

### `daily_match_commentaries` Tablosu

```sql
CREATE TABLE daily_match_commentaries (
    id SERIAL PRIMARY KEY,
    match_id BIGINT UNIQUE,
    match_date VARCHAR(20),
    match_time VARCHAR(20),
    country VARCHAR(100),
    league VARCHAR(200),
    home_team_id INTEGER,
    home_team_name VARCHAR(200),
    away_team_id INTEGER,
    away_team_name VARCHAR(200),
    commentary_json JSONB,              -- 📦 TÜM YORUMLAR BURADA
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### JSON Yapısı

```json
{
  "match_info": {
    "match_id": 123456,
    "match_date": "05/11/25",
    "match_time": "19:00",
    "timezone": "+03",
    "country": "Türkiye",
    "league": "Süper Lig",
    "season_id": 12345,
    "round": 11,
    "week": 45,
    "stadium_id": 123,
    "description": "..."
  },
  "home_team": {
    "team_id": 3052,
    "team_name": "Fenerbahçe",
    "is_home": true,
    "commentary": "286 sütun analizi...",
    "generated_at": "2025-11-05T10:30:00"
  },
  "away_team": {
    "team_id": 3091,
    "team_name": "Hatayspor",
    "is_home": false,
    "commentary": "286 sütun analizi...",
    "generated_at": "2025-11-05T10:30:00"
  },
  "analysis_summary": {
    "match_description": "Türkiye Süper Lig - 11. Hafta",
    "venue": "Fenerbahçe Stadyumu",
    "kickoff": "05/11/25 19:00 (+03)",
    "ai_prompt_ready": true,
    "rag_optimized": true
  },
  "metadata": {
    "generated_at": "2025-11-05T10:30:00",
    "system_version": "2.1",
    "data_source": "team_sum_last_10",
    "commentary_type": "comprehensive_286_columns"
  }
}
```

---

## 🔧 Gelişmiş Özellikler

### Dosya Export

```bash
# JSON dosyası olarak kaydet
python modules/commentary/daily_commentary.py --file

# Veritabanı yerine sadece dosya
python modules/commentary/daily_commentary.py --no-db --file
```

### Farklı Analiz Tablosu

```bash
# team_sum_last_5 kullan
python modules/commentary/daily_commentary.py --table team_sum_last_5

# team_sum_home_last_10 kullan  
python modules/commentary/daily_commentary.py --table team_sum_home_last_10
```

---

## 📊 Örnek Çıktı

```
================================================================================
🎯 GÜNLÜK MAÇ YORUM İŞLEME SİSTEMİ
================================================================================

📅 Tarih: 05/11/25
✅ 18 maç bulundu!

================================================================================

📊 Maç 1/18: Baku Sporting vs Cabrayil
   🏆 Lig: Azerbaycan - Birinci Lig
   ⏰ Saat: 13:00 (+03)
   🔄 Yorumlar oluşturuluyor...
   ✅ Başarılı!

📊 Maç 2/18: ENERGETIK MINGECHEVIR vs Safa
   🏆 Lig: Azerbaycan - Birinci Lig
   ⏰ Saat: 13:00 (+03)
   🔄 Yorumlar oluşturuluyor...
   ✅ Başarılı!

...

================================================================================
✅ İŞLEM TAMAMLANDI!
📊 Toplam 18/18 maç başarıyla işlendi.
================================================================================

================================================================================
📊 ÖZET RAPOR
================================================================================
✅ İşlenen Maç Sayısı: 18
💾 Veritabanına Kaydedildi: Evet
📁 Dosyaya Kaydedildi: Hayır

📈 LİG DAĞILIMI:
   Azerbaycan - Birinci Lig: 3 maç
   Ermenistan - Birinci Lig: 3 maç
   Hırvatistan - Prva NL: 1 maç
   Kuzey Makedonya - Prva Liga: 2 maç
   Türkiye - Süper Lig: 5 maç
   İngiltere - Premier League: 4 maç
================================================================================
```

---

## 🎯 Python API Kullanımı

```python
from database.source_connection import SourceConnection
from database.analytics_connection import AnalyticsConnection
from modules.commentary.daily_matches import process_daily_matches

# Veritabanı bağlantıları
source_db = SourceConnection()
analytics_db = AnalyticsConnection()

# Bugünün maçlarını işle
commentaries = process_daily_matches(
    source_db, 
    analytics_db,
    match_date=None,  # None = bugün
    table_name='team_sum_last_10',
    save_to_db=True
)

# Sonuçlar
print(f"✅ {len(commentaries)} maç işlendi")

# Belirli bir maç
match = commentaries[0]
print(match['match_info']['description'])
print(match['home_team']['commentary'])
```

---

## 🔍 Veritabanı Sorguları

### Bugünün Tüm Maç Yorumlarını Çek

```sql
SELECT 
    match_id,
    home_team_name,
    away_team_name,
    commentary_json
FROM daily_match_commentaries
WHERE match_date = '05/11/25'
ORDER BY match_time;
```

### Belirli Bir Takımın Tüm Maç Yorumları

```sql
SELECT 
    match_date,
    match_time,
    home_team_name,
    away_team_name,
    commentary_json
FROM daily_match_commentaries
WHERE home_team_id = 3052 OR away_team_id = 3052
ORDER BY match_date DESC;
```

### JSON İçinde Arama

```sql
SELECT 
    match_id,
    commentary_json->>'match_description'
FROM daily_match_commentaries
WHERE commentary_json->'match_info'->>'country' = 'Türkiye'
AND commentary_json->'match_info'->>'league' = 'Süper Lig';
```

---

## 🎯 Sistem Akışı

```
1. Kullanıcı tarihi girer
   ↓
2. current_week_fixtures tablosundan maçlar çekilir
   ↓
3. Her maç için:
   - Ev sahibi takım analizi (286 sütun)
   - Deplasman takımı analizi (286 sütun)
   - Maç bilgileri eklenir
   ↓
4. JSON oluşturulur:
   {
     match_info: {...},
     home_team: {commentary: "..."},
     away_team: {commentary: "..."}
   }
   ↓
5. Veritabanına kaydedilir (JSONB)
   ↓
6. Dosyaya export (opsiyonel)
```

---

## ✅ Avantajlar

- ✨ **Otomatik İşlem**: Sadece tarih gir, sistem her şeyi yapar
- 💾 **Merkezi Depo**: Tüm yorumlar tek tabloda JSON formatında
- 🔍 **Hızlı Arama**: match_id, tarih, takım bazında sorgulama
- 📊 **Kapsamlı Analiz**: 286 sütunlu detaylı takım yorumları
- 🤖 **AI Hazır**: RAG ve prompt engineering için optimize
- 🌍 **Çoklu Lig**: Tüm ülke ve ligler desteklenir
- ⏰ **Zaman Bilgisi**: Maç saati, timezone, unix timestamp
- 🏆 **Lig Detayları**: Sezon, hafta, round bilgileri

---

## 📝 Notlar

- Tarih formatı: **DD/MM/YY** (örn: 05/11/25)
- Timezone bilgileri maç verisinden otomatik alınır
- JSON sütunu JSONB olarak saklanır (PostgreSQL optimize)
- UPSERT desteği: Aynı maç tekrar işlenirse güncellenir
- Index'ler: match_id, match_date, team_id'ler üzerinde

---

## 🚀 Gelecek Geliştirmeler

- [ ] Real-time maç skorları entegrasyonu
- [ ] AI tahmin modeli entegrasyonu
- [ ] Webhook sistemi (yeni maç eklenince otomatik işlem)
- [ ] API endpoint'leri (REST/GraphQL)
- [ ] Dashboard ve görselleştirme
- [ ] Multi-language support

---

**Version:** 2.1.0  
**Date:** November 5, 2025  
**Author:** Spradar Analytics Team
