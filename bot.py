import telebot
import random
import string
from supabase import create_client, Client

# 1. ADIMDA NOT ETTİĞİNİZ BİLGİLERİ VE TELEGRAM TOKENİNİZİ BURAYA YAZIN:
BOT_TOKEN = "8882583341:AAHDzXSsSTwNEK5KNaV2OddQt6fkrh1a0AQ"
SUPABASE_URL = "https://fzkrirthqwpospkodfcv.supabase.co" # Kendi URL'niz
SUPABASE_KEY = "sb_publishable_RPFAoyA9kkWhkOlhciaeZg_-iDoRYWu" # Kendi uzun şifreniz

bot = telebot.TeleBot(BOT_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@bot.message_handler(commands=['kargo'])
def kargo_olustur(message):
    try:
        # Mesajı satırlara bölüyoruz
        satirlar = message.text.split('\n')
        
        # Kullanıcı eksik satır girdi mi kontrolü
        if len(satirlar) < 5:
            bot.reply_to(message, "❌ Eksik format! Lütfen şu şekilde yazın:\n\n/kargo\nAlıcı Adı Soyadı\nAdres Bilgisi\nTeslim Tarihi (GG.AA.YYYY)\nGönderici Firma")
            return
            
        alici = satirlar[1].strip()
        adres = satirlar[2].strip()
        teslim_tarihi = satirlar[3].strip()
        etiket = satirlar[4].strip()
        
        # 11 haneli rastgele takip numarası üretiyoruz
        takip_no = ''.join(random.choices(string.digits, k=11))

        # Supabase bulut veritabanına kaydediyoruz
        data = {
            "takip_no": takip_no,
            "alici": alici,
            "adres": adres,
            "teslim_tarihi": teslim_tarihi,
            "etiket": etiket
        }
        supabase.table("siparisler").insert(data).execute()

        # Web sitenizin linkini buraya bağlayacağız (Şimdilik örnek yazıyoruz)
        site_link = f"https://create-similar-website.vercel.app/takip/{takip_no}"

        cevap = f"✅ Kargo Başarıyla Kaydedildi!\n\n📦 Takip Kodu: {takip_no}\n🔗 Takip Linki: {site_link}"
        bot.reply_to(message, cevap)

    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    print("Bot başlatıldı, mesaj bekleniyor...")
    bot.polling(none_stop=True)