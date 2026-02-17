import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# 1. Coba ambil URL dari Secrets (Utama untuk Cloud)
db_url = st.secrets.get("DATABASE_URL")

# 2. Jika tidak ada di Secrets (berarti sedang di Lokal), ambil dari Environment Variable
if not db_url:
    # Kita bungkus dotenv agar jika librarynya tidak ada, aplikasi tidak mati
    try:
        from dotenv import load_dotenv
        load_dotenv()
        db_url = os.getenv("DATABASE_URL")
    except ImportError:
        pass

# 3. Koneksi ke Database
if db_url:
    engine = create_engine(db_url)
else:
    st.error("Koneksi Database tidak ditemukan. Cek Secrets atau file .env!")
    st.stop()