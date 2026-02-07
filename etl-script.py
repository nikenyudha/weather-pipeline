import pandas as pd
import requests
from sqlalchemy import create_engine
import time # Tambahkan ini untuk mengatur jeda waktu

# Setting koneksi
engine = create_engine('postgresql://postgres:password123@localhost:5435/weather_db')

def run_etl():
    try:
        # 1. EXTRACT
        print(f"[{pd.Timestamp.now()}] Mengambil data...")
        url = "https://api.open-meteo.com/v1/forecast?latitude=-6.2146&longitude=106.8451&current_weather=true"
        response = requests.get(url).json()
        data = response['current_weather']

        # 2. TRANSFORM
        df = pd.DataFrame([data])
        df['city'] = 'Jakarta'
        df['extracted_at'] = pd.Timestamp.now()

        # 3. LOAD
        df.to_sql('jakarta_weather', engine, if_exists='append', index=False)
        print("✅ Data berhasil masuk ke Database.")
    except Exception as e:
        print(f"❌ Error terjadi: {e}")

# LOOP UTAMA
if __name__ == "__main__":
    print("🚀 Pipeline Otomatis Dimulai... (Tekan Ctrl+C untuk berhenti)")
    while True:
        run_etl()
        time.sleep(30) # Tunggu 30 detik sebelum mengambil data lagi