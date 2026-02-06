import pandas as pd
import requests
from sqlalchemy import create_engine

# 1. EXTRACT: Ambil data cuaca Jakarta (Open-Meteo API)
print("Mengambil data...")
url = "https://api.open-meteo.com/v1/forecast?latitude=-6.2146&longitude=106.8451&current_weather=true"
response = requests.get(url).json()
data = response['current_weather']

# 2. TRANSFORM: Ubah ke DataFrame & rapikan format
df = pd.DataFrame([data])
df['city'] = 'Jakarta'
df['extracted_at'] = pd.Timestamp.now()
print("Data berhasil dirapikan:")
print(df)

# 3. LOAD: Kirim ke PostgreSQL
# Format: postgresql://user:password@localhost:port/database
# Gunakan user 'postgres' dan port '5435'
engine = create_engine('postgresql://postgres:password123@localhost:5435/weather_db')
df.to_sql('jakarta_weather', engine, if_exists='append', index=False)
print("Data berhasil disimpan ke Database!")