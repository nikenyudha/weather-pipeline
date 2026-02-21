# 🌤️ Multi city Real-time Weather Data Pipeline
This project is a simple **End-to-End Data Pipeline** for capturing, processing, and visualizing real-time weather data.

# 🌸Streamlit link 
 [https://city-weather-dashboard.streamlit.app/]


## 🏗️ Architecture
Sistem ini terdiri dari tiga komponen utama:
1. **Extraction & Transformation (Python):** Mengambil data dari Open-Meteo API dan membersihkannya menggunakan Pandas.
2. **Storage (PostgreSQL & Docker):** Menyimpan data hasil olahan ke dalam database relasional yang terisolasi di dalam container Docker.
3. **Visualization (Streamlit):** Dashboard interaktif untuk memantau tren suhu secara langsung dari database.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Database:** PostgreSQL 15 (Dockerized)
* **Libraries:** Pandas, SQLAlchemy, Psycopg2, Streamlit, Requests
* **Infrastructure:** Docker & Docker Compose

## 👩‍💻 Author
**Niken Larasati**
**(Data Scientist & Writer)**
