# 🌤️ Multi-City Real-Time Weather Data Pipeline

An automated End-to-End Data Engineering project that captures, processes, stores, and visualizes real-time weather data from multiple cities.
This project demonstrates practical implementation of data extraction, transformation, containerized database storage, and interactive dashboard deployment.

## 🔗 Live Dashboard:
[https://city-weather-dashboard.streamlit.app/]

## 🚀 Project Overview

This pipeline automatically retrieves real-time weather data from the Open-Meteo API and processes it into a structured format for analytical use. The cleaned data is stored in a Dockerized PostgreSQL database and visualized through an interactive Streamlit dashboard.
The system runs with zero manual intervention, ensuring continuous data availability and monitoring.

## 🏗️ Architecture

The system consists of three main components:
### 1️⃣ Extraction & Transformation (Python)

- Fetches real-time weather data from Open-Meteo API
- Cleans and transforms raw JSON data using Pandas
- Prepares structured data ready for database storage

### 2️⃣ Storage (Neon Serverless PostgreSQL)

- Stores processed data in Neon (serverless PostgreSQL cloud database)
- Fully managed cloud database with automatic scaling
- Secure connection via SSL
- Eliminates infrastructure management overhead

### 3️⃣ Visualization (Streamlit)

- Interactive dashboard connected directly to PostgreSQL
- Displays temperature trends across multiple cities
- Enables real-time monitoring and analysis

### 🛠️ Tech Stack
   ### Language
       Python 3.x

### Database
- PostgreSQL (Neon Serverless Cloud)
- Infrastructure
- Neon Cloud Platform
- Docker (for local development)

### Libraries
- Pandas
- SQLAlchemy
- Psycopg2
- Requests
- Streamlit
- Infrastructure
- Docker
- Docker Compose

### 📊 Key Features
- ✅ Automated real-time data ingestion
- ✅ End-to-end ETL pipeline
- ✅ Containerized relational database
- ✅ Cloud-deployed interactive dashboard
- ✅ Scalable architecture for additional cities

## 👩‍💻 Author
**Niken Larasati**
(Data Scientist | Data Engineering Enthusiast | Writer)

