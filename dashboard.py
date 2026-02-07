import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
#from dotenv import load_dotenv

db_url = st.secrets.get("DATABASE_URL", None)

if db_url:
    st.write("Database connected")
else:
    st.warning("DATABASE_URL not found")
engine = create_engine(db_url)
# ------------------------------

# 1. Setup Streamlit Page
st.set_page_config(page_title="Multi-City Weather Monitor", layout="wide")

st.title("🌤️ Multi-City Real-time Weather Dashboard")
st.write("Data ini diambil secara otomatis dari PostgreSQL (Docker).")

# Fungsi untuk ambil data dari DB
def get_data():
    query = "SELECT * FROM jakarta_weather ORDER BY extracted_at DESC"
    return pd.read_sql(query, engine)

# --- AMBIL DATA AWAL (Penting agar 'df' terdefinisi sebelum dipakai) ---
df_init = get_data()

# 2. Sidebar untuk Kontrol
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (detik)", 5, 60, 10)

# Cek apakah database ada isinya
if not df_init.empty:
    all_cities = sorted(df_init['city'].unique())
else:
    all_cities = ["No Data Found"]

# Dropdown pilihan kota
selected_city = st.sidebar.selectbox("Pilih Kota yang Ingin Dipantau", all_cities)

# 3. Layout Dashboard (Main Content)
placeholder = st.empty()

while True:
    with placeholder.container():
        # REFRESH DATA: Ambil data terbaru setiap siklus
        df = get_data()

        if not df.empty:
            # FILTER: Hanya ambil data untuk kota yang dipilih di sidebar
            df_filtered = df[df['city'] == selected_city]

            if not df_filtered.empty:
                # Ambil data terbaru untuk kota terpilih
                latest_data = df_filtered.iloc[0]
                latest_temp = latest_data['temperature']
                latest_time = latest_data['extracted_at']

                # Tampilan Metric Utama
                col1, col2 = st.columns(2)
                col1.metric(f"Suhu di {selected_city}", f"{latest_temp} °C")
                col2.metric("Terakhir Update", latest_time.strftime("%H:%M:%S"))

                # Tampilan Grafik Tren (The DS Side!)
                st.subheader(f"Tren Suhu: {selected_city}")
                # Kita urutkan berdasarkan waktu agar garis grafiknya benar
                df_chart = df_filtered.set_index('extracted_at').sort_index()
                st.line_chart(df_chart['temperature'])

                # Tampilan Tabel Data Mentah (Khusus kota tersebut)
                st.subheader(f"Log Data Terakhir ({selected_city})")
                st.dataframe(df_filtered.head(10))
            else:
                st.warning(f"Belum ada data untuk kota {selected_city}")
        else:
            st.error("Database kosong! Pastikan etl-script.py sudah berjalan.")

        time.sleep(refresh_rate)

