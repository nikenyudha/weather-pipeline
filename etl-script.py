import os
import time
import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine

# ==============================
# 1. LOAD ENV (OPTIONAL)
# ==============================
if "DATABASE_URL" not in st.secrets:
    st.error("DATABASE_URL tidak ditemukan di secrets.")
    st.stop()

db_url = st.secrets["DATABASE_URL"]
engine = create_engine(db_url)

# ==============================
# 3. CITY CONFIG
# ==============================
CITIES = {
    "Jakarta": {"lat": -6.2146, "lon": 106.8451},
    "Bogor": {"lat": -6.5952, "lon": 106.8167},
    "Surabaya": {"lat": -7.2575, "lon": 112.7521},
    "Kediri": {"lat": -7.8014, "lon": 112.0014},
    "Malang": {"lat": -7.9833, "lon": 112.6333},
    "Medan": {"lat": 3.5952, "lon": 98.6722},
    "Palembang": {"lat": -2.9761, "lon": 104.7754},
    "Padang": {"lat": -0.9471, "lon": 100.4172},
    "Pekanbaru": {"lat": 0.5333, "lon": 101.4500},
    "Batam": {"lat": 1.1500, "lon": 104.0000},
    "Banda Aceh": {"lat": 5.5500, "lon": 95.3167},
    "Pontianak": {"lat": 0.0333, "lon": 109.3333},
    "Palangka Raya": {"lat": -2.2167, "lon": 113.9167},
    "Balikpapan": {"lat": -1.2667, "lon": 116.8333},
    "Samarinda": {"lat": -0.5000, "lon": 117.1500},
    "Banjarmasin": {"lat": -3.3167, "lon": 114.5833},
    "Samarinda": {"lat": -0.5000, "lon": 117.1500},
    "Tanjung Selor": {"lat": 2.7333, "lon": 117.3000},
    "Manado": {"lat": 1.5000, "lon": 124.8500},
    "Palu": {"lat": -0.9000, "lon": 119.8500},
    "Makassar": {"lat": -5.1500, "lon": 119.4333},
    "Bandung": {"lat": -6.9175, "lon": 107.6191},
    "Yogyakarta": {"lat": -7.7956, "lon": 110.3695},
    "Semarang": {"lat": -6.9667, "lon": 110.4167},
    "Mataram": {"lat": -8.5833, "lon": 116.1167},
    "Maluku": {"lat": -3.3667, "lon": 128.1833},
    "Lombok": {"lat": -8.6500, "lon": 116.2167},
    "Denpasar": {"lat": -8.6500, "lon": 115.2167},
    "Gorontalo": {"lat": 0.5333, "lon": 123.0667},
    "Mamuju": {"lat": -2.3000, "lon": 118.1500},
    "Sofifi": {"lat": -0.6833, "lon": 131.2167},
    "Ambon": {"lat": -3.7000, "lon": 128.2000},
    "Manokwari": {"lat": -0.8667, "lon": 134.0833},
    "Jayapura": {"lat": -2.5333, "lon": 140.7167},

}

# ==============================
# 4. ETL FUNCTION
# ==============================
def run_etl():
    print(f"\n--- ETL START | {pd.Timestamp.now()} ---")

    for city, coord in CITIES.items():
        try:
            # EXTRACT
            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={coord['lat']}"
                f"&longitude={coord['lon']}"
                "&current_weather=true"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            weather = response.json()["current_weather"]

            # TRANSFORM
            df = pd.DataFrame([weather])
            df["city"] = city
            df["extracted_at"] = pd.Timestamp.utcnow()

            # LOAD
            df.to_sql(
                "jakarta_weather",
                engine,
                if_exists="append",
                index=False
            )

            print(f"✅ {city} inserted")

        except Exception as e:
            print(f"❌ {city} failed: {e}")

    print(f"--- ETL END | {pd.Timestamp.now()} ---\n")

# ==============================
# 5. ENTRY POINT
# ==============================
if __name__ == "__main__":
    while True:
        run_etl()
        print("😴 Menunggu 10 menit untuk pengambilan data berikutnya...")
        time.sleep(600) # 600 detik = 10 menit

    
