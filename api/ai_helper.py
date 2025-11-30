"""
🤖 Together AI Helper - Maç analizi için AI sohbet
"""

from together import Together
from django.conf import settings


class MatchAIChat:
    """Together AI ile maç analizi sohbeti"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or getattr(settings, 'TOGETHER_API_KEY', '07e297e19eaabe78c4ae52006f8d7ea67d6470727fff514aba20559fb273ea31')
        self.client = Together(api_key=self.api_key)
        self.model = "Qwen/Qwen2.5-72B-Instruct-Turbo"  # Türkçe için optimize - 3x ucuz!
    
    def get_match_context(self, match_data):
        """
        Match verisinden AI için context oluştur - TOKEN LİMİTİ OPTİMİZE EDİLDİ
        
        Together AI Limit: inputs + max_new_tokens <= 8193
        Strateji: 
        - combined_prompt'un en önemli kısımlarını al (ilk 6000 karakter ~ 1500 token)
        - max_tokens: 4000 (daha uzun ve detaylı yanıtlar)
        - Toplam: ~5500 token (limit içinde)
        
        Args:
            match_data: DailyMatchCommentary objesi veya dict
        
        Returns:
            str: AI'ya gönderilecek context metni
        """
        if hasattr(match_data, 'commentary_json'):
            # Django model objesi
            metadata = match_data.commentary_json.get('metadata', {})
            combined_prompt = match_data.commentary_json.get('combined_prompt', '')
            
            
            
            context = f"""Sen futbol maç analistisin. SADECE verilen istatistiklere dayalı cevap ver.

⚠️ ÖNEMLİ KURALLAR:
1. SADECE aşağıdaki maç verisini kullan
2. Bilmediğin bir şeyi ASLA uydurma
3. Lig sıralaması, şampiyonluk sayısı gibi genel bilgileri SÖYLEME (veride yok)
4. Kullanıcı genel soru sorarsa: "Bu soru maç verileriyle ilgili değil, sadece bu maç hakkında cevap verebilirim." de

MAÇ: {match_data.home_team_name} vs {match_data.away_team_name}
LİG: {match_data.league} ({match_data.country})
TARİH: {match_data.match_date} {match_data.match_time}

DETAYLI ANALİZ (SADECE BU VERİYİ KULLAN):
{combined_prompt}

⚠️ MUTLAKA TÜRKÇE CEVAP VER! İngilizce kesinlikle yasak!

🎨 FORMATLAMA KURALLARI:
- Başlıklar için ### kullan (örn: ### Fenerbahçe:)
- Önemli kelimeleri **kalın** yap (örn: **önemli**)
- Madde işaretleri için - kullan (örn: - Form: ...)
- Uygun emojiler ekle (⚽ 🏆 📊 🔥 ⚠️ 💪 🎯 📈 📉 ✅ ❌ 🟢 🔴 🟡)
"""
        else:
            # Dict objesi
            context = f"""
MAÇ: {match_data.get('home_team_name')} vs {match_data.get('away_team_name')}
LİG: {match_data.get('league')} ({match_data.get('country')})
TARİH: {match_data.get('match_date')} {match_data.get('match_time')}

Sen profesyonel bir futbol bahis analistisin. Kullanıcının sorularını yanıtla.
"""
        
        return context
    
    def chat(self, user_message, match_context, chat_history=None):
        """
        AI ile sohbet et
        
        Args:
            user_message (str): Kullanıcının sorusu
            match_context (str): Maç context bilgisi
            chat_history (list): Önceki mesajlar [{'role': 'user', 'content': '...'}, ...]
        
        Returns:
            str: AI'nın yanıtı
        """
        messages = []
        
        # System message (maç context)
        messages.append({
            "role": "system",
            "content": match_context
        })
        
        # Önceki chat geçmişi
        if chat_history:
            for msg in chat_history[-5:]:  # Son 5 mesaj
                messages.append(msg)
        
        # Yeni kullanıcı mesajı
        messages.append({
            "role": "system",
            "content": """⚠️ ÖNEMLİ: 
1. Cevabın TAMAMEN Türkçe olmalı! İngilizce kelime kullanma!
2. SADECE yukarıdaki maç verilerini kullan - başka bilgi ekleme!
3. Cevabında MUTLAKA emoji kullan (⚽🏆📊🔥💪🎯📈✅❌🟢🔴)
4. Başlıklar için ### kullan
5. Önemli kelimeleri **kalın** yap
6. Madde işaretleri için - kullan
7. Genel sorulara (lig sıralaması, şampiyonluk sayısı vb.) cevap verme, sadece maç istatistiklerine odaklan!"""
        })
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Türkçe enforcement için retry mekanizması
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=4000,  # Daha uzun ve detaylı cevaplar
                    temperature=0.6,  # Qwen için optimize
                    top_p=0.9,
                )
                
                ai_response = response.choices[0].message.content
                
                # İngilizce kontrol
                english_words = ['goal', 'match', 'team', 'player', 'win', 'lose', 'score', 'draw', 
                                'considering', 'performance', 'prediction', 'crucial', 'statistics',
                                'defense', 'attack', 'half', 'outcome', 'solid', 'weak', 'tend']
                
                has_english = any(f' {word} ' in ai_response.lower() for word in english_words)
                
                if not has_english:
                    # Türkçe cevap geldi!
                    return ai_response
                elif attempt < max_retries - 1:
                    # Tekrar dene
                    messages.append({
                        "role": "system",
                        "content": "⚠️ HATA: İngilizce kelime kullandın! Aynı cevabı TAMAMEN TÜRKÇE ver!"
                    })
                else:
                    # Son deneme, translation uygula
                    return self._translate_to_turkish(ai_response)
            
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return f"❌ AI yanıt verirken hata oluştu: {str(e)}"
        
        return ai_response
    
    def _translate_to_turkish(self, text):
        """İngilizce kelimeleri Türkçeye çevir (fallback)"""
        translations = {
            " goal ": " gol ", " goals ": " goller ",
            " match ": " maç ", " matches ": " maçlar ",
            " team ": " takım ", " teams ": " takımlar ",
            " player ": " oyuncu ", " players ": " oyuncular ",
            " win ": " kazanma ", " wins ": " kazanır ",
            " lose ": " kaybetme ", " loses ": " kaybeder ",
            " score ": " skor ", " scores ": " skorlar ",
            " draw ": " beraberlik ", " draws ": " beraberlikler ",
            " half ": " yarı ", " first half ": " ilk yarı ", " second half ": " ikinci yarı ",
            " defense ": " savunma ", " attack ": " atak ",
            " performance ": " performans ", " statistics ": " istatistikler ",
            " prediction ": " tahmin ", " outcome ": " sonuç ",
            " solid ": " sağlam ", " weak ": " zayıf ",
            " tend ": " eğilim ", " considering ": " göz önüne alındığında ",
            " crucial ": " kritik ", " competitive ": " rekabetçi ",
        }
        
        result = text.lower()
        for eng, tr in translations.items():
            result = result.replace(eng, tr)
        
        return result
    
    def generate_match_summary(self, match_data):
        """
        Maç için özet analiz oluştur
        
        Args:
            match_data: DailyMatchCommentary objesi
        
        Returns:
            str: Maç özeti
        """
        context = self.get_match_context(match_data)
        
        prompt = """

bu maç hakkında kullanıcılara kaliteli ve istatistiklere uygun cevaplar ver , kullanıcılara yapacakları bahisler konusunda yardımcı olabilecek analizler yap , Türkçe cevap ver.
Takımların güçlü ve zayıf yönlerini, maçın kritik anlarını ve olası sonuçları değerlendir. takımların ilk yarı ve maç sonucu kgvar,alt üst gibi analizler yap.

"""
        
        return self.chat(prompt, context)


# Global instance
ai_chat = MatchAIChat()
