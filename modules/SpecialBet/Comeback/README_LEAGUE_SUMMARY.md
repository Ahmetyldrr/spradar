# 🏆 League Comeback Summary System

## 📋 Genel Bakış

Bu sistem, **comprehensive_comeback_analysis** tablosundaki tüm maç yorumlarını **sezon/lig bazında** tek bir JSON içinde toplar ve **league_comeback_summary** tablosuna kaydeder.

---

## 🗄️ Veritabanı Tablosu: `league_comeback_summary`

### Tablo Yapısı

```sql
CREATE TABLE league_comeback_summary (
    season_id INTEGER PRIMARY KEY,
    season_name TEXT,
    league_name TEXT,
    league_id INTEGER,
    match_count INTEGER,
    matches_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Kolonlar

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| `season_id` | INTEGER | Sezon ID (Primary Key) |
| `season_name` | TEXT | Sezon adı (örn: "Season 134371") |
| `league_name` | TEXT | Lig adı (örn: "Premier League", "La Liga") |
| `league_id` | INTEGER | Lig ID |
| `match_count` | INTEGER | Bu sezonda kaç maç var |
| `matches_json` | JSONB | Tüm maçların yorumları (JSON array) |
| `created_at` | TIMESTAMP | Kayıt oluşturma zamanı |

---

## 📦 JSON Yapısı

Her sezon için `matches_json` kolonu bir **array** içerir:

```json
[
  {
    "match_id": 63167877,
    "home_team": {
      "team_id": 1234,
      "team_name": "Manchester United",
      "comeback_score": 15.0
    },
    "away_team": {
      "team_id": 5678,
      "team_name": "Liverpool",
      "comeback_score": 20.0
    },
    "match_date": "2025-11-08",
    "combined_comeback_score": 17.5,
    "data_quality": "OK",
    "commentary": {
      "combined_prompt": "... 15,000+ karakter yorum ...",
      "home_commentary": { ... },
      "away_commentary": { ... },
      "match_interaction": { ... },
      "ai_question": "...",
      "metadata": { ... }
    }
  },
  {
    "match_id": 63167878,
    ...
  }
]
```

---

## 🚀 Kullanım

### 1. Tabloyu Oluştur ve Doldur

```bash
python modules/SpecialBet/Comeback/aggregate_by_league.py
```

**Çıktı:**
```
✅ league_comeback_summary tablosu hazır!
📊 Toplam 1,067 maç yorumu bulundu
📋 Sezon sayısı: 215
✅ 215 sezon verisi league_comeback_summary tablosuna kaydedildi!

🏆 Toplam Sezon: 215
⚽ Toplam Maç: 1,067
📈 Ortalama Maç/Sezon: 5.0
```

---

## 📊 SQL Sorguları

### Tüm Ligleri Listele

```sql
SELECT 
    season_id, 
    league_name, 
    season_name, 
    match_count 
FROM league_comeback_summary 
ORDER BY match_count DESC;
```

### Belirli Bir Ligin Tüm Maçlarını Al

```sql
SELECT matches_json 
FROM league_comeback_summary 
WHERE league_name = 'Premier League';
```

### En Fazla Maç İçeren 10 Sezon

```sql
SELECT 
    season_name,
    league_name,
    match_count
FROM league_comeback_summary
ORDER BY match_count DESC
LIMIT 10;
```

### JSON İçindeki Maçları Sorgula

```sql
SELECT 
    season_name,
    league_name,
    jsonb_array_length(matches_json) as match_count,
    matches_json->0->>'match_id' as first_match_id,
    matches_json->0->'home_team'->>'team_name' as first_home_team
FROM league_comeback_summary
WHERE match_count > 10;
```

### Yüksek Comeback Skorlu Maçları Filtrele

```sql
SELECT 
    season_name,
    league_name,
    match_count,
    (
        SELECT COUNT(*)
        FROM jsonb_array_elements(matches_json) as match
        WHERE (match->>'combined_comeback_score')::float > 10
    ) as high_score_matches
FROM league_comeback_summary
WHERE match_count > 5
ORDER BY high_score_matches DESC;
```

---

## 🔧 Script Detayları

### `aggregate_by_league.py`

**Fonksiyonlar:**

1. **`create_league_summary_table()`**
   - `league_comeback_summary` tablosunu oluşturur
   - Index'leri ekler

2. **`get_season_info_from_matches(season_id, match_df)`**
   - Sezon bilgilerini match verilerinden çıkarır
   - `season_name`, `league_name`, `league_id` döndürür

3. **`aggregate_by_season()`**
   - `comprehensive_comeback_analysis` tablosundan verileri alır
   - `season_id`'ye göre gruplar
   - Tüm maçları JSON array'e dönüştürür
   - `league_comeback_summary` tablosuna kaydeder

4. **`main()`**
   - Tüm işlemleri koordine eder

---

## 📈 İstatistikler

**Mevcut Durum:**
- ✅ 215 sezon işlendi
- ✅ 1,067 maç yorumu birleştirildi
- ✅ Ortalama 5.0 maç/sezon
- ✅ En fazla maç: 47 (bir sezonda)
- ✅ Her sezon için tam yorumlar JSONB içinde

---

## 🎯 Avantajlar

1. **Tek JSON**: Tüm sezon verileri tek sorguda alınabilir
2. **Performans**: JSONB indeksleme ile hızlı sorgulama
3. **Esneklik**: JSON içinde istediğiniz alanı sorgulayabilirsiniz
4. **AI Entegrasyonu**: Yorumlar doğrudan AI'ya gönderilebilir
5. **Veri Bütünlüğü**: Tüm commentary verileri korunur

---

## 💡 Örnek Kullanım Senaryoları

### 1. Bir Ligin Tüm Yorumlarını Al

```python
from database.analytics_connection import AnalyticsConnection
import json

analytics = AnalyticsConnection()

result = analytics.query("""
    SELECT matches_json 
    FROM league_comeback_summary 
    WHERE season_id = 134371
""")

matches = result[0][0]  # JSONB direkt Python list olarak gelir

for match in matches:
    print(f"Match: {match['home_team']['team_name']} vs {match['away_team']['team_name']}")
    print(f"Comeback Score: {match['combined_comeback_score']}")
    
    # Yorumu al
    commentary = json.loads(match['commentary'])
    print(f"Commentary: {commentary['combined_prompt'][:200]}...")
    print()
```

### 2. En İyi Comeback Maçlarını Bul

```python
result = analytics.query("""
    SELECT 
        season_name,
        match_element->>'match_id' as match_id,
        match_element->'home_team'->>'team_name' as home,
        match_element->'away_team'->>'team_name' as away,
        (match_element->>'combined_comeback_score')::float as score
    FROM league_comeback_summary,
    LATERAL jsonb_array_elements(matches_json) as match_element
    WHERE (match_element->>'combined_comeback_score')::float > 15
    ORDER BY score DESC
    LIMIT 10
""")

for row in result:
    print(f"{row[2]} vs {row[3]}: {row[4]}")
```

### 3. Sezona Göre Filtrele ve AI'ya Gönder

```python
import openai

# Sezonun tüm yorumlarını al
result = analytics.query("""
    SELECT matches_json 
    FROM league_comeback_summary 
    WHERE league_name LIKE '%Premier%'
    ORDER BY match_count DESC
    LIMIT 1
""")

matches = result[0][0]

# En yüksek skorlu maçı bul
best_match = max(matches, key=lambda x: x['combined_comeback_score'])

# Yorumu parse et
commentary = json.loads(best_match['commentary'])

# AI'ya gönder
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"Analyze this comeback potential:\n\n{commentary['combined_prompt']}"
    }]
)

print(response.choices[0].message.content)
```

---

## ✅ Sonuç

Bu sistem sayesinde:
- ✅ Tüm comeback yorumları lig/sezon bazında organize edildi
- ✅ Tek bir JSON içinde tüm veriler toplandı
- ✅ PostgreSQL JSONB ile hızlı sorgulama sağlandı
- ✅ AI entegrasyonu için hazır veri yapısı oluşturuldu

**Tablo:** `league_comeback_summary`  
**Script:** `aggregate_by_league.py`  
**Veri Kaynağı:** `comprehensive_comeback_analysis`
