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
    "Surabaya": {"lat": -7.2575, "lon": 112.7521},
    "Medan": {"lat": 3.5952, "lon": 98.6722},
    "Bandung": {"lat": -6.9175, "lon": 107.6191},
    "Semarang": {"lat": -6.9667, "lon": 110.4167},
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
    run_etl()
