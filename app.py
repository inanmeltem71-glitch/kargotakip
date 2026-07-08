import os
from flask import Flask, render_template, abort
from supabase import create_client, Client
from datetime import datetime

app = Flask(__name__)
application = app  # Vercel'in uygulamayı tanıması için gerekli

# SUPABASE BİLGİLERİ
SUPABASE_URL = "https://fzkrirthqwpospkodfcv.supabase.co"
SUPABASE_KEY = "sb_publishable_RPFAoyA9kkWhkOlhciaeZg_-iDoRYWu"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def asama_hesapla(teslim_tarihi_str):
    try:
        bugun = datetime.now().date()
        teslim_tarihi = datetime.strptime(teslim_tarihi_str, "%d.%m.%Y").date()
        kalan_gun = (teslim_tarihi - bugun).days

        if kalan_gun > 3: return "Kabul Edildi", 1
        elif kalan_gun == 3: return "Aktarma Merkezinde", 2
        elif kalan_gun == 2: return "Yolda / Transfer Sürecinde", 3
        elif kalan_gun == 1: return "Teslimat Şubesinde", 4
        elif kalan_gun == 0: return "Dağıtımda (Bugün Teslim)", 5
        else: return "Teslim Edildi", 6
    except Exception:
        return "Kabul Edildi", 1

@app.route('/')
def index():
    # Burası ana sayfan (örneğin takip numarası girme ekranın)
    return render_template('takip.html')

@app.route('/takip/<takip_no>')
def takip_sayfasi(takip_no):
    response = supabase.table("siparisler").select("*").eq("takip_no", takip_no).execute()
    
    if not response.data:
        abort(404, description="Takip numarası bulunamadı.")
        
    kargo = response.data[0]
    durum_metni, asama_id = asama_hesapla(kargo["teslim_tarihi"])
    
    veri = {
        "takip_no": kargo["takip_no"],
        "alici": kargo["alici"],
        "adres": kargo["adres"],
        "teslim_tarihi": kargo["teslim_tarihi"],
        "etiket": kargo["etiket"],
        "durum": durum_metni,
        "asama": asama_id
    }
    
    return render_template('takip.html', kargo=veri)

if name == '__main__':
    app.run(debug=True)