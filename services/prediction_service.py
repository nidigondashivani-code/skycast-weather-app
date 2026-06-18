import pandas as pd
from sklearn.linear_model import LinearRegression
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.weather_dao import get_weather_history

def predict_temperature(city):
    """Predicts tomorrow's temperature using Linear Regression based on history or API backfill."""
    # Get historical data
    logs = get_weather_history(city)
    
    if len(logs) >= 5:
        # Convert DB logs to Pandas DataFrame
        data = [{
            "temperature": log.temperature,
            "humidity": log.humidity,
            "wind_speed": log.wind_speed,
            "pressure": log.pressure,
            "time": log.fetched_time.timestamp()
        } for log in logs]
        df = pd.DataFrame(data)
        df = df.sort_values(by="time")
    else:
        # Not enough DB data, fetch 72 hours of real historical data from Open-Meteo
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_data = requests.get(geo_url).json()
            if not geo_data.get("results"): return None
            
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            
            hist_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,surface_pressure,windspeed_10m&past_days=3"
            hist_data = requests.get(hist_url).json().get("hourly", {})
            
            if not hist_data: return None
            
            df = pd.DataFrame({
                "temperature": hist_data["temperature_2m"][:72],
                "humidity": hist_data["relative_humidity_2m"][:72],
                "pressure": hist_data["surface_pressure"][:72],
                "wind_speed": hist_data["windspeed_10m"][:72],
            })
            df = df.dropna()
            if len(df) < 5: return None
        except Exception as e:
            print(f"Error fetching ML backfill data: {e}")
            return None
    
    # Machine Learning Model
    X = df[["humidity", "wind_speed", "pressure"]]
    y = df["temperature"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict based on the most recent condition
    latest = df.iloc[-1]
    next_features = pd.DataFrame({
        "humidity": [latest["humidity"]],
        "wind_speed": [latest["wind_speed"]],
        "pressure": [latest["pressure"]]
    })
    
    prediction = model.predict(next_features)
    return round(prediction[0], 2)
