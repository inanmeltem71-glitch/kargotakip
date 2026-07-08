from flask import Flask, render_template

app = Flask(__name__)
application = app  # Vercel'in uygulamayı tanıması için bu satır çok önemli!

@app.route('/')
def index():
    return render_template('takip.html')

if name == '__main__':
    app.run(debug=True)
import os
from flask import Flask, render_template, abort
from supabase import create_client, Client
from datetime import datetime

app = Flask(__name__)

# SUPABASE BİLGİLERİNİZİ BURAYA DA YAPIŞTIRIN:
SUPABASE_URL = "https://fzkrirthqwpospkodfcv.supabase.co"  # Kendi URL'niz
SUPABASE_KEY = "sb_publishable_RPFAoyA9kkWhkOlhciaeZg_-iDoRYWu"         # Kendi Key'iniz

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def asama_hesapla(kayit_tarihi_str, teslim_tarihi_str):
    """ Günler ilerledikçe aşamayı otomatik olarak bir adım ileri taşır """
    try:
        # Supabase'den gelen tarihi ve kullanıcının girdiği teslim tarihini tarihe çeviriyoruz
        bugun = datetime.now().date()
        teslim_tarihi = datetime.strptime(teslim_tarihi_str, "%d.%m.%Y").date()
        
        kalan_gun = (teslim_tarihi - bugun).days

        if kalan_gun > 3:
            return "Kabul Edildi", 1
        elif kalan_gun == 3:
            return "Aktarma Merkezinde", 2
        elif kalan_gun == 2:
            return "Yolda / Transfer Sürecinde", 3
        elif kalan_gun == 1:
            return "Teslimat Şubesinde", 4
        elif kalan_gun == 0:
            return "Dağıtımda (Bugün Teslim)", 5
        else:
            return "Teslim Edildi", 6
    except Exception:
        return "Kabul Edildi", 1

@app.route('/takip/<takip_no>')
def takip_sayfasi(takip_no):
    # Supabase'den kargo bilgilerini çekiyoruz
    response = supabase.table("siparisler").select("*").eq("takip_no", takip_no).execute()
    
    if not response.data:
        abort(404, description="Takip numarası bulunamadı.")
        
    kargo = response.data[0]
    
    # Otomatik aşama durumunu hesaplatıyoruz
    # Eğer tablonuzda oluşturulma tarihi yoksa manuel 'created_at' yerine bugünü baz alabiliriz
    durum_metni, asama_id = asama_hesapla("01.07.2026", kargo["teslim_tarihi"])
    
    veri = {
        "takip_no": kargo["takip_no"],
        "alici": kargo["alici"],
        "adres": kargo["adres"],
        "teslim_tarihi": kargo["teslim_tarihi"],
        "etiket": kargo["etiket"],
        "durum": durum_metni,
        "asama": asama_id
    }
    
    # Sadece 'veri' değişkenini 'kargo' olarak gönderiyoruz:
    return render_template('takip.html', kargo=veri)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
