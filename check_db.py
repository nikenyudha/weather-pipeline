import pandas as pd
from sqlalchemy import create_engine

# Gunakan koneksi yang sama dengan script ETL tadi
engine = create_engine('postgresql://postgres:password123@localhost:5435/weather_db')

# Query sederhana untuk melihat 5 data terbaru
df = pd.read_sql('SELECT * FROM jakarta_weather ORDER BY extracted_at DESC LIMIT 5', engine)

print("Isi Database Kamu:")
print(df)