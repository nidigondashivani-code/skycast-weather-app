import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Database Configuration
# Using SQLite for easy portability across different laptops without needing MySQL Server
DB_PATH = "sqlite:///weather.db"

# Cities to monitor (Global Network)
DEFAULT_GLOBAL_CITIES = "New York,London,Tokyo,Sydney,Paris,Dubai,Rio de Janeiro,Cairo,Beijing,Moscow,Toronto,Johannesburg,Mumbai,Singapore,Mexico City"
CITIES = os.getenv("CITIES", DEFAULT_GLOBAL_CITIES).split(",")

# Alert Thresholds
TEMP_UPPER_THRESHOLD = 40.0 # Celsius
TEMP_LOWER_THRESHOLD = 5.0  # Celsius
ALERT_CONDITIONS = ["Thunderstorm", "Rain", "Snow", "Extreme"]

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
ALERT_RECIPIENTS = os.getenv("ALERT_RECIPIENTS", "").split(",")
