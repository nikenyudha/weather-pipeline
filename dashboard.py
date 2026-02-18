import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

st.set_page_config(page_title="Multi-City Weather", page_icon="🌍", layout="wide")

# --- KONEKSI DATABASE ---
db_url = st.secrets.get("DATABASE_URL")
if not db_url:
    from dotenv import load_dotenv
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)

# --- AMBIL DAFTAR KOTA YANG ADA DI DATABASE ---
@st.cache_data(ttl=60)
def get_city_list():
    # Mengambil nama-nama kota unik yang sudah pernah masuk ke database
    query = "SELECT DISTINCT city FROM jakarta_weather"
    cities = pd.read_sql(query, engine)
    return cities['city'].tolist()

# --- AMBIL DATA BERDASARKAN KOTA YANG DIPILIH ---
def get_weather_data(city):
    query = f"SELECT * FROM jakarta_weather WHERE city = '{city}' ORDER BY time DESC"
    df = pd.read_sql(query, engine)
    df['time'] = pd.to_datetime(df['time'])
    return df

# --- UI SIDEBAR (DROPDOWN) ---
st.sidebar.header("Konfigurasi")
available_cities = get_city_list()
selected_city = st.sidebar.selectbox("Pilih Kota yang Ingin Dipantau:", available_cities)

# --- TAMPILAN UTAMA ---
st.title(f"📊 Dashboard Cuaca: {selected_city}")

try:
    data = get_weather_data(selected_city)
    
    if not data.empty:
        # Metrik
        latest = data.iloc[0]
        c1, c2 = st.columns(2)
        c1.metric("Suhu", f"{latest['temperature']} °C")
        c2.metric("Angin", f"{latest['windspeed']} km/h")

        # Grafik
        st.subheader(f"📈 Tren Suhu di {selected_city}")
        st.line_chart(data=data.sort_values('time'), x='time', y='temperature')
    else:
        st.warning(f"Belum ada data untuk kota {selected_city}")

except Exception as e:
    st.error(f"Error: {e}")

st.subheader("📊 Ringkasan Statistik")
col1, col2, col3 = st.columns(3)
col1.metric("Suhu Rata-rata", f"{data['temperature'].mean():.1f} °C")
col2.metric("Suhu Tertinggi", f"{data['temperature'].max()} °C")
col3.metric("Suhu Terendah", f"{data['temperature'].min()} °C")

st.subheader("🔍 Korelasi: Suhu vs Kecepatan Angin")
# Membuat scatter plot untuk melihat hubungan dua variabel
st.scatter_chart(data=data, x='temperature', y='windspeed')

# Menghitung angka korelasi (Opsional)
corr = data['temperature'].corr(data['windspeed'])
st.write(f"Nilai Korelasi: {corr:.2f} (Jika mendekati 1 atau -1, hubungannya kuat)")

