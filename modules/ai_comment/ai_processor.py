#!/usr/bin/env python3
"""
🤖 AI COMMENTARY PROCESSOR
==========================

daily_match_commentaries tablosundan yorumları alır,
DeepSeek AI'ye gönderir ve sonuçları ai_respond tablosuna kaydeder.

Usage:
    python modules/ai_comment/ai_processor.py 05/11/25
    python modules/ai_comment/ai_processor.py 05/11/25 --limit 5
"""

import sys
import os
import json
import time  # Sleep için
from datetime import datetime
from openai import OpenAI

# Path setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database.analytics_connection import AnalyticsConnection

# OpenAI API Key
OPENAI_API_KEY = "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"


class AICommentaryProcessor:
    """OpenAI GPT-4o ile yorum işleme sistemi"""
    
    def __init__(self):
        self.analytics_db = AnalyticsConnection()
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # GPT-4o: 128K token, EN GÜÇLÜ MODEL, $2.50 input / $10 output
        self.model = "gpt-4o"
        self.max_prompt_chars = 30000  # 30K karakter = TÜM VERİ + ekstra alan
    
    def get_commentaries_by_date(self, match_date: str, limit: int = None):
        """
        Belirli tarihteki TÜM yorumları al
        
        Args:
            match_date: Maç tarihi (DD/MM/YY formatında)
            limit: Maksimum kayıt sayısı
        
        Returns:
            List of commentary records
        """
        query = """
            SELECT 
                id,
                match_id,
                match_date,
                home_team_id,
                away_team_id,
                home_team_name,
                away_team_name,
                league,
                country,
                commentary_json->>'combined_prompt' as combined_prompt,
                commentary_json->'metadata' as metadata
            FROM daily_match_commentaries
            WHERE match_date = %s
            ORDER BY match_time
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        df = self.analytics_db.query_df(query, (match_date,))
        
        if df is None or df.empty:
            return []
        
        return df.to_dict('records')
    
    def process_with_ai(self, combined_prompt: str, metadata: dict) -> str:
        """
        Yorumu AI'ye gönder ve analiz et
        
        Args:
            combined_prompt: Takım yorumu
            metadata: Maç metadata'sı
        
        Returns:
            AI'nin ürettiği yorum
        """
        # Combined prompt'u kısalt - 20K karakter (Llama 3.3 için yeterli)
        if len(combined_prompt) > self.max_prompt_chars:
            shortened_prompt = combined_prompt[:self.max_prompt_chars] + "\n\n[...devamı kısaltıldı]"
        else:
            shortened_prompt = combined_prompt
        
        system_prompt = """Sen profesyonel bir Türk futbol yorumcususun. SADECE TÜRKÇE YAZ!
Takım istatistiklerini analiz edip maç öncesi yorum yap.

SADECE JSON formatında yanıt ver:
{
    "analysis": "Türkçe analiz metni (3-4 paragraf)",
    "predicted_score": "10-1",
    "predicted_score_ht": "6-0",
    "predictions": {
        "ms1": true, "ms2": false, "ms0": false,
        "kg_var": true, "ust_25": true, "alt_25": false,
        "iy_ust_05": true, "iy_alt_05": false,
        "iy_ms1": true, "iy_ms2": false, "iy_ms0": false
    },
    "confidence": "yüksek"
}
"""

        user_prompt = f"""TÜRKÇE YORUM YAP (SADECE JSON):

{shortened_prompt}

İki takımı karşılaştır, güçlü/zayıf yönlerini belirt, tahmin yap.
JSON formatında yanıt ver!"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000,  # Daha uzun ve detaylı cevaplar
                response_format={"type": "json_object"}  # JSON Mode - zorunlu JSON döner
            )
            
            ai_text = response.choices[0].message.content.strip()
            
            # <think> taglerini temizle
            if '<think>' in ai_text:
                import re
                ai_text = re.sub(r'<think>.*?</think>', '', ai_text, flags=re.DOTALL)
                ai_text = ai_text.strip()
            
            return ai_text
        
        except Exception as e:
            print(f"      ❌ AI hatası: {e}")
            return f"ERROR: {str(e)}"
    
    def save_ai_response(self, commentary_record: dict, ai_response: str) -> bool:
        """
        AI yorumunu veritabanına kaydet
        
        Args:
            commentary_record: Orijinal yorum kaydı
            ai_response: AI'nin ürettiği yorum (JSON formatında)
        
        Returns:
            Başarılı ise True
        """
        # AI response'u parse et - artık direkt JSON
        try:
            response_json = json.loads(ai_response)
            analysis_text = response_json.get('analysis', ai_response)
            predicted_score = response_json.get('predicted_score')
            predicted_score_ht = response_json.get('predicted_score_ht')
            predictions = response_json.get('predictions', {})
            
            # Full predictions JSON
            predictions_json = {
                'predicted_score': predicted_score,
                'predicted_score_ht': predicted_score_ht,
                'predictions': predictions,
                'confidence': response_json.get('confidence', 'orta')
            }
        except json.JSONDecodeError as e:
            print(f"      ⚠️ JSON parse hatası: {e}")
            analysis_text = ai_response
            predicted_score = None
            predicted_score_ht = None
            predictions_json = {"error": "JSON parse failed", "raw": ai_response[:500]}
        
        # INSERT: Tablo temiz, direkt ekle
        insert_query = """
            INSERT INTO ai_respond (
                commentary_id,
                match_id,
                match_date,
                home_team_id,
                away_team_id,
                home_team_name,
                away_team_name,
                league,
                country,
                original_prompt,
                ai_response,
                predictions_json,
                predicted_score,
                predicted_score_ht,
                model_name,
                metadata,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Metadata'yı JSON string'e çevir
        metadata_json = commentary_record.get('metadata', {})
        if isinstance(metadata_json, str):
            metadata_json = json.loads(metadata_json)
        
        params = (
            commentary_record['id'],
            commentary_record['match_id'],
            commentary_record['match_date'],
            commentary_record['home_team_id'],
            commentary_record['away_team_id'],
            commentary_record['home_team_name'],
            commentary_record['away_team_name'],
            commentary_record.get('league', ''),
            commentary_record.get('country', ''),
            commentary_record['combined_prompt'],
            analysis_text,  # Sadece analiz metni
            json.dumps(predictions_json) if predictions_json else None,  # JSON tahminler
            predicted_score,  # Tahmini skor
            predicted_score_ht,  # Tahmini ilk yarı skoru
            self.model,
            json.dumps(metadata_json),
            datetime.now()
        )
        
        return self.analytics_db.execute_query(insert_query, params)
    
    def clear_ai_responses(self):
        """ai_respond tablosunu temizle"""
        truncate_query = "TRUNCATE TABLE ai_respond RESTART IDENTITY CASCADE"
        return self.analytics_db.execute_query(truncate_query)
    
    def process_date(self, match_date: str, limit: int = None):
        """
        Belirli tarihteki tüm yorumları işle
        
        Args:
            match_date: Maç tarihi (DD/MM/YY)
            limit: Maksimum işlenecek kayıt sayısı
        """
        print("=" * 80)
        print("🤖 AI COMMENTARY PROCESSOR")
        print("=" * 80)
        print(f"📅 Tarih: {match_date}")
        print(f"🤖 Model: {self.model}")
        if limit:
            print(f"⚠️  Limit: {limit} maç (test modu)")
        print("=" * 80)
        print()
        
        # Tabloyu temizle
        print("🗑️  Önceki AI yorumları temizleniyor...")
        if self.clear_ai_responses():
            print("✅ Tablo temizlendi!")
        else:
            print("⚠️  Tablo temizlenemedi ama devam ediliyor...")
        print()
        
        # Yorumları al
        print("📊 Yorumlar yükleniyor...")
        commentaries = self.get_commentaries_by_date(match_date, limit)
        
        if not commentaries:
            print(f"ℹ️  {match_date} tarihinde işlenecek yorum yok!")
            print("   (Tüm yorumlar zaten AI'ye gönderilmiş olabilir)")
            return
        
        print(f"✅ {len(commentaries)} yorum bulundu!")
        print()
        
        # Her yorumu işle
        success_count = 0
        error_count = 0
        
        for idx, commentary in enumerate(commentaries, 1):
            match_info = f"{commentary['home_team_name']} vs {commentary['away_team_name']}"
            print(f"📊 Maç {idx}/{len(commentaries)}: {match_info}")
            print(f"   🏆 Lig: {commentary.get('country', 'N/A')} - {commentary.get('league', 'N/A')}")
            
            # Prompt kontrolü
            if not commentary.get('combined_prompt'):
                print(f"   ⏭️  Combined prompt bulunamadı, atlanıyor...")
                error_count += 1
                print()
                continue
            
            try:
                # Metadata'yı parse et
                metadata = commentary.get('metadata', {})
                if isinstance(metadata, str):
                    metadata = json.loads(metadata)
                
                # AI'ye gönder
                print(f"   🤖 AI'ye gönderiliyor...")
                ai_response = self.process_with_ai(
                    commentary['combined_prompt'],
                    metadata
                )
                
                if ai_response.startswith("ERROR:"):
                    print(f"   ❌ AI hatası!")
                    error_count += 1
                    print()
                    continue
                
                # Veritabanına kaydet
                print(f"   💾 Veritabanına kaydediliyor...")
                if self.save_ai_response(commentary, ai_response):
                    print(f"   ✅ Başarılı! ({len(ai_response)} karakter)")
                    success_count += 1
                else:
                    print(f"   ❌ Kayıt hatası!")
                    error_count += 1
                
            except Exception as e:
                print(f"   ❌ Hata: {e}")
                error_count += 1
            
            print()
        
        # Özet
        print("=" * 80)
        print("✅ İŞLEM TAMAMLANDI!")
        print("=" * 80)
        print(f"📊 Başarılı: {success_count}/{len(commentaries)}")
        if error_count > 0:
            print(f"❌ Hatalı: {error_count}/{len(commentaries)}")
        print("=" * 80)


def main():
    """Ana program"""
    print("=" * 80)
    print("🤖 AI YORUM İŞLEME SİSTEMİ")
    print("=" * 80)
    print()
    
    # Kullanıcıdan tarih al
    match_date = input("📅 Maç tarihi girin (DD/MM/YY formatında, örn: 05/11/25): ").strip()
    
    if not match_date:
        print("❌ Tarih girmediniz!")
        return
    
    # Limit sorusu
    limit_input = input("🔢 Kaç maç işlensin? (Enter = hepsi): ").strip()
    limit = int(limit_input) if limit_input else None
    
    print()
    
    # İşlemciyi başlat
    processor = AICommentaryProcessor()
    processor.process_date(match_date, limit)


if __name__ == '__main__':
    main()
