import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Weather Cloud Dashboard", page_icon="🌤️", layout="wide")

# --- KONEKSI DATABASE (HYBRID) ---
db_url = st.secrets.get("DATABASE_URL")
if not db_url:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        db_url = os.getenv("DATABASE_URL")
    except ImportError:
        pass

if not db_url:
    st.error("Konfigurasi Database tidak ditemukan!")
    st.stop()

engine = create_engine(db_url)

# --- FUNGSI AMBIL DATA ---
@st.cache_data(ttl=60) # Cache selama 1 menit supaya tidak bolak-balik nembak Neon
def get_data():
    query = "SELECT * FROM jakarta_weather ORDER BY time DESC"
    df = pd.read_sql(query, engine)
    df['time'] = pd.to_datetime(df['time']) # Pastikan format waktu benar
    return df

# --- UI DASHBOARD ---
st.title("🌤️ Real-time Weather Pipeline")
st.markdown("Data ini diambil langsung dari **Neon Cloud Database** yang diupdate oleh robot ETL kamu.")

try:
    data = get_data()

    # 1. BARIS METRIK (HIGHLIGHT)
    latest = data.iloc[0] # Ambil data paling baru
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Suhu Saat Ini", f"{latest['temperature']} °C", delta_color="normal")
    with col2:
        st.metric("Kecepatan Angin", f"{latest['windspeed']} km/h")
    with col3:
        st.metric("Lokasi", latest['city'])

    st.divider()

    # 2. GRAFIK TREN SUHU
    st.subheader("📈 Tren Suhu Terkini")
    # Urutkan waktu dari lama ke baru khusus untuk grafik
    chart_data = data.sort_values('time')
    st.line_chart(data=chart_data, x='time', y='temperature')

    # 3. TABEL DETAIL
    with st.expander("🔎 Lihat Detail Data Mentah"):
        st.dataframe(data, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat visualisasi: {e}")

# Tombol Refresh Manual
if st.button('🔄 Update Data Terbaru'):
    st.rerun()