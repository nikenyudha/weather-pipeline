import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

st.title("Weather Pipeline Test")

# Ambil URL
db_url = st.secrets.get("DATABASE_URL")

if not db_url:
    st.error("Kunci DATABASE_URL tidak ditemukan di Secrets!")
else:
    try:
        engine = create_engine(db_url)
        # Coba ambil 1 baris saja untuk tes koneksi
        df = pd.read_sql("SELECT * FROM jakarta_weather LIMIT 1", engine)
        st.write("✅ Koneksi Berhasil! Ini data contoh:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")