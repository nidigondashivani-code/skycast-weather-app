# 🌤️ SkyCast Weather Intelligence System

A real-time, globally scalable Weather Monitoring and Alert System built with Python and Streamlit. This project fetches 100% exact, live meteorological satellite data for any city in the world using the Open-Meteo API. It includes historical tracking, an interactive dashboard, and a Machine Learning model (Scikit-Learn) to predict tomorrow's temperatures.

## ✨ Features
* **Zero Configuration:** Uses SQLite and free public APIs. No API keys or database servers are required!
* **Global Monitoring:** Tracks 15 major global cities automatically in the background.
* **Live Location & Search:** Automatically detects your local weather and allows you to search for any city worldwide.
* **ML Predictions:** Dynamically backfills historical training data to generate high-confidence temperature forecasts.
* **Alerts & Reports:** Triggers alerts for extreme conditions and allows exporting complete weather telemetry as CSVs.

---

## 🚀 How to Setup on ANY Laptop

Because this project was designed for maximum portability, setting it up on a new laptop takes less than 2 minutes.

### 1. Copy the Project Folder
Transfer the entire `weather_app` folder (the one containing this README) to the new laptop via a USB drive, Google Drive, or GitHub.

### 2. Install Python
Ensure Python is installed on the new laptop. You can download it from [python.org](https://www.python.org/downloads/).

### 3. Install Dependencies
Open a terminal (Command Prompt or PowerShell) inside the `weather_app` folder and run:
```bash
pip install -r requirements.txt
```

### 4. Run the Background Monitor (Optional but recommended)
To enable background data tracking and alerts, run the daemon script in your terminal:
```bash
python main.py
```
*(Leave this terminal window open in the background)*

### 5. Launch the Dashboard
Open a **new** terminal inside the `weather_app` folder and run:
```bash
streamlit run app.py
```
Your browser will automatically open `http://localhost:8501` to display the SkyCast dashboard!

---

## 📁 Project Structure
* `app.py`: The main Streamlit interactive dashboard.
* `main.py`: The automated background script that syncs data every 1 hour.
* `database/`: Contains the SQLite setup and SQLAlchemy models.
* `services/`: Contains all business logic (Weather fetching, ML Predictions, Alerts, Reports).
* `weather.db`: The local database file containing all historical telemetry.
