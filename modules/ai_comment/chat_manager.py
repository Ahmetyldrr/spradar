"""
Chat Manager
Match bazlı AI sohbet yöneticisi - chat history saklama ve yönetme
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from together import Together


class ChatManager:
    """Match bazlı chat session yöneticisi"""
    
    def __init__(self, api_key: str, db_connection=None):
        """
        Args:
            api_key: Together AI API key
            db_connection: Database bağlantısı (AnalyticsConnection)
        """
        self.client = Together(api_key=api_key)
        self.model = "Qwen/Qwen2.5-72B-Instruct-Turbo"
        self.db = db_connection
        
        # System prompt - Kısa ve net
        self.system_prompt = """Sen futbol analistisin. SADECE Türkçe cevap ver.

Görev: Maç analizi, 3-5 cümle, Türkçe.

Örnek: "Monaco ikinci yarıda daha fazla atak yapacak. Lens savunmada kalabilir. Maç 2-2 bitebilir."
"""
    
    def get_match_context(self, match_id: int) -> Optional[str]:
        """
        Match ID'ye göre combined_prompt'u al
        
        Args:
            match_id: Match ID
            
        Returns:
            Combined prompt string veya None
        """
        if not self.db:
            return None
        
        query = """
            SELECT commentary_json->>'combined_prompt' as combined_prompt
            FROM daily_match_commentaries
            WHERE match_id = %s
            LIMIT 1
        """
        
        result = self.db.query_df(query, (match_id,))
        
        if result is None or result.empty:
            return None
        
        return result.iloc[0]['combined_prompt']
    
    def get_chat_history(self, match_id: int, limit: int = 20) -> List[Dict]:
        """
        Match ID'ye göre chat geçmişini al
        
        Args:
            match_id: Match ID
            limit: Maksimum mesaj sayısı
            
        Returns:
            List of chat messages [{"role": "user"/"assistant", "content": "..."}]
        """
        if not self.db:
            return []
        
        query = """
            SELECT 
                user_message,
                ai_response,
                created_at
            FROM match_chat_history
            WHERE match_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        
        df = self.db.query_df(query, (match_id, limit))
        
        if df is None or df.empty:
            return []
        
        # Reverse order (oldest first)
        messages = []
        for _, row in df.iloc[::-1].iterrows():
            messages.append({"role": "user", "content": row['user_message']})
            messages.append({"role": "assistant", "content": row['ai_response']})
        
        return messages
    
    def save_chat_message(self, match_id: int, user_message: str, ai_response: str) -> bool:
        """
        Chat mesajını veritabanına kaydet
        
        Args:
            match_id: Match ID
            user_message: Kullanıcı mesajı
            ai_response: AI yanıtı
            
        Returns:
            Başarılı ise True
        """
        if not self.db:
            return False
        
        query = """
            INSERT INTO match_chat_history (
                match_id,
                user_message,
                ai_response,
                created_at
            ) VALUES (%s, %s, %s, %s)
        """
        
        return self.db.execute_query(
            query,
            (match_id, user_message, ai_response, datetime.now())
        )
    
    def chat(
        self,
        match_id: int,
        user_message: str,
        include_context: bool = True,
        save_history: bool = True
    ) -> str:
        """
        Kullanıcı ile sohbet et
        
        Args:
            match_id: Match ID
            user_message: Kullanıcı mesajı
            include_context: Match context'i ekle (ilk mesajda)
            save_history: History'e kaydet
            
        Returns:
            AI yanıtı
        """
        # Messages listesi oluştur - TÜRKÇE UYARISI İLE BAŞLA
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Match context ekle (ilk mesajda veya istenirse)
        if include_context:
            match_context = self.get_match_context(match_id)
            if match_context:
                # Context'i TAMAMEN ekle - LİMİT YOK!
                context_message = f"""İstatistikler:

{match_context}"""
                messages.append({"role": "user", "content": context_message})
                # Context'ten hemen sonra GÜÇLÜ Türkçe uyarısı
                messages.append({"role": "system", "content": "🚨 UYARI: Yukarıdaki verileri analiz ederken SADECE TÜRKÇE yaz! goal→gol, match→maç, team→takım"})
        
        # Chat history ekle
        chat_history = self.get_chat_history(match_id, limit=10)
        messages.extend(chat_history)
        
        # HER MESAJDAN HEMEN ÖNCE TÜRKÇE UYARISI
        messages.append({"role": "system", "content": "⚠️ ÖNEMLİ: Cevabın TAMAMEN Türkçe olmalı! İngilizce kelime yasak!"})
        
        # Kullanıcı mesajını ekle
        messages.append({"role": "user", "content": user_message})
        
        # AI'ye gönder
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,  # Daha uzun ve detaylı cevaplar
                temperature=0.4,  # Qwen için optimal
                top_p=0.8,  # Daha tutarlı yanıtlar
            )
            
            ai_response = response.choices[0].message.content
            
            # OTOMATİK İNGİLİZCE → TÜRKÇE ÇEVİRİ
            translations = {
                " goal ": " gol ",
                " goals ": " gol ",
                " match ": " maç ",
                " matches ": " maçlar ",
                " team ": " takım ",
                " teams ": " takımlar ",
                " win ": " galibiyet ",
                " wins ": " galibiyetler ",
                " draw ": " beraberlik ",
                " draws ": " beraberlikler ",
                " loss ": " mağlubiyet ",
                " losses ": " mağlubiyetler ",
                " score ": " skor ",
                " scores ": " skorlar ",
                " half ": " yarı ",
                " halves ": " yarılar ",
                " first ": " ilk ",
                " second ": " ikinci ",
                " will ": " olacak ",
                " might ": " olabilir ",
                " can ": " yapabilir ",
                " could ": " yapabilir ",
                " should ": " yapmalı ",
                " would ": " yapardı ",
                " based ": " göre ",
                " analysis ": " analiz ",
                " predict ": " tahmin ediyorum ",
                " prediction ": " tahmin ",
                " likely ": " muhtemelen ",
                " possible ": " olası ",
                " scenario ": " senaryo ",
                " attack ": " hücum ",
                " defense ": " savunma ",
                " leading ": " önde ",
                " forward ": " ileri ",
                " push ": " baskı ",
                " maintain ": " sürdür ",
                " focus ": " odaklan ",
                " defending ": " savunma yapma ",
                " trying ": " deneme ",
                " counter ": " kontra ",
                " solid ": " sağlam ",
                " conceded ": " yenildi ",
                " protect ": " koru ",
                " create ": " oluştur ",
                " scoring ": " gol atma ",
                " opportunities ": " fırsatlar ",
                " level ": " seviye ",
                " decent ": " iyi ",
                " exploit ": " istismar et ",
                " vulnerable ": " savunmasız ",
                " average ": " ortalama ",
                " tendency ": " eğilim ",
                " comeback ": " geri dönüş ",
                " record ": " rekor ",
                " positions ": " pozisyonlar ",
                " early ": " erken ",
                " turn ": " dön ",
                " around ": " etrafında ",
                " factors ": " faktörler ",
                " assumes ": " varsayar ",
                " continue ": " devam et ",
                " thrilling ": " heyecanlı ",
                " sharing ": " paylaşma ",
                " points ": " puanlar ",
                " agree ": " katılıyorum ",
                " predictions ": " tahminler ",
                " what ": " ne ",
                " think ": " düşünüyorum ",
                " exciting ": " heyecan verici ",
                " happen ": " olur ",
                " review ": " inceleme ",
                " surprise ": " sürpriz ",
                " given ": " göre ",
                " their ": " onların ",
                " this ": " bu ",
                " which ": " hangi ",
                " some ": " bazı ",
                " here ": " burada ",
                " with ": " ile ",
                " has ": " var ",
                " been ": " oldu ",
                " only ": " sadece ",
                " they ": " onlar ",
                "The ": "Maç ",
                "What ": "Ne ",
                "I ": "Ben ",
            }
            
            # Cevabı Türkçe'ye çevir
            ai_response_lower = ai_response.lower()
            for eng, tr in translations.items():
                ai_response = ai_response.replace(eng, tr)
                ai_response = ai_response.replace(eng.capitalize(), tr.capitalize())
                ai_response = ai_response.replace(eng.upper(), tr.upper())
            
            # TÜRKÇE KONTROLÜ - GENİŞLETİLMİŞ İngilizce kelime listesi
            english_words = [
                "goal", "match", "team", "win", "draw", "loss", "score", "half", "full", "time", 
                "over", "under", "first", "second", "attack", "defense", "might", "will", "can",
                "leading", "prediction", "likely", "possible", "scenario", "based", "data", "analysis",
                "excellent", "form", "inconsistent", "performance", "dominant", "advantage", "consistent",
                "overall", "season", "statistics", "maintain", "focus", "defending", "trying", "counter",
                "solid", "conceded", "park", "bus", "protect", "push", "forward", "create", "scoring",
                "opportunities", "level", "decent", "exploit", "vulnerable", "average", "tendency",
                "high-scoring", "comeback", "record", "positions", "early", "turn", "around", "factors",
                "assumes", "continue", "thrilling", "sharing", "points", "agree", "predictions",
                "what", "think", "exciting", "predict", "happen", "review", "surprise", "given",
                "their", "this", "not", "which", "some", "here", "are", "with", "has", "been",
                "only", "they", "and", "the", "to", "is", "for", "on", "in", "at", "by", "from"
            ]
            
            # Kelime bazlı kontrol (case-insensitive)
            response_lower = ai_response.lower()
            detected_english = [word for word in english_words if f" {word} " in f" {response_lower} "]
            
            if detected_english:
                # İngilizce kelime tespit edildi, 3 kez daha dene
                print(f"⚠️ İngilizce kelimeler tespit edildi: {detected_english[:5]}")
                
                for retry_attempt in range(3):  # 3 KEZ DENE
                    messages.append({"role": "assistant", "content": ai_response})
                    
                    # Her denemede daha sert uyarı
                    if retry_attempt == 0:
                        warning = "⚠️ UYARI: İngilizce kelimeler var! SADECE TÜRKÇE yaz!"
                    elif retry_attempt == 1:
                        warning = "🚨 HATA! HALA İngilizce! TAMAMEN TÜRKÇE YAZ!"
                    else:
                        warning = "❌ SON UYARI! İNGİLİZCE YASAK! TÜRKÇE YAZ!"
                    
                    messages.append({"role": "system", "content": f"""{warning}

İngilizce: {', '.join(detected_english[:8])}
Türkçe: goal→gol, match→maç, team→takım, win→galibiyet, draw→beraberlik, score→skor, half→yarı

TÜRKÇE YAZ!"""})
                    
                    # Tekrar dene - temperature daha düşük
                    retry_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=4000,  # Daha uzun ve detaylı cevaplar
                        temperature=0.4,  # Qwen için optimal
                        top_p=0.8,
                    )
                    ai_response = retry_response.choices[0].message.content
                    
                    # Tekrar kontrol et
                    response_lower = ai_response.lower()
                    detected_english = [word for word in english_words if f" {word} " in f" {response_lower} "]
                    
                    if not detected_english:
                        print(f"✅ {retry_attempt + 1}. denemede Türkçe cevap alındı!")
                        break
                else:
                    print(f"❌ 3 denemeden sonra hala İngilizce: {detected_english[:5]}")
                    # Son çare: Cevabı otomatik çevir
                    for eng, tr in translations.items():
                        ai_response = ai_response.replace(eng, tr)
                        ai_response = ai_response.replace(eng.capitalize(), tr.capitalize())
                    print(f"✅ Otomatik çeviri yapıldı")

            
            # History'e kaydet
            if save_history:
                self.save_chat_message(match_id, user_message, ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Üzgünüm, bir hata oluştu: {str(e)}"
            if save_history:
                self.save_chat_message(match_id, user_message, error_msg)
            return error_msg
    
    def clear_chat_history(self, match_id: int) -> bool:
        """
        Match ID'ye göre chat geçmişini temizle
        
        Args:
            match_id: Match ID
            
        Returns:
            Başarılı ise True
        """
        if not self.db:
            return False
        
        query = "DELETE FROM match_chat_history WHERE match_id = %s"
        return self.db.execute_query(query, (match_id,))
    
    def get_chat_stats(self, match_id: int) -> Dict:
        """
        Match için chat istatistikleri
        
        Args:
            match_id: Match ID
            
        Returns:
            {total_messages, first_message_at, last_message_at}
        """
        if not self.db:
            return {}
        
        query = """
            SELECT 
                COUNT(*) as total_messages,
                MIN(created_at) as first_message_at,
                MAX(created_at) as last_message_at
            FROM match_chat_history
            WHERE match_id = %s
        """
        
        df = self.db.query_df(query, (match_id,))
        
        if df is None or df.empty:
            return {"total_messages": 0}
        
        return df.iloc[0].to_dict()
