import os
import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time

# 1. Setting Koneksi
load_dotenv()
db_url = os.getenv("DATABASE_URL")

# CEK ERROR
print(f"DEBUG: Link Database yang terbaca adalah -> {db_url}")

if db_url is None:
    print("❌ ERROR: File .env tidak terbaca atau DATABASE_URL kosong!")
else:
    engine = create_engine(db_url)

# 2. Daftar Kota (Pindahkan ke luar agar rapi)
cities = {
    'Jakarta': {'lat': -6.2146, 'lon': 106.8451},
    'Surabaya': {'lat': -7.2575, 'lon': 112.7521},
    'Medan': {'lat': 3.5952, 'lon': 98.6722}
}

def run_etl():
    print(f"\n--- [{pd.Timestamp.now()}] Memulai Siklus Ingestion ---")
    
    for city_name, coord in cities.items():
        try:
            # A. EXTRACT
            print(f"Mengambil data untuk {city_name}...")
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coord['lat']}&longitude={coord['lon']}&current_weather=true"
            response = requests.get(url).json()
            data = response['current_weather'] # Sekarang 'data' didefinisikan di sini

            # B. TRANSFORM
            df = pd.DataFrame([data])
            df['city'] = city_name
            df['extracted_at'] = pd.Timestamp.now()

            # C. LOAD
            # Kita tetap pakai nama tabel 'jakarta_weather' supaya dashboard kamu tidak error, 
            # tapi isinya sekarang sudah macam-macam kota.
            df.to_sql('jakarta_weather', engine, if_exists='append', index=False)
            print(f"✅ {city_name} berhasil disimpan.")

        except Exception as e:
            print(f"❌ Gagal memproses {city_name}: {e}")

# 3. LOOP UTAMA
if __name__ == "__main__":
    print("🚀 Multi-City Pipeline Aktif... (Tekan Ctrl+C untuk berhenti)")
    while True:
        run_etl()
        print(f"Siklus selesai. Menunggu 30 detik...")
        time.sleep(30)