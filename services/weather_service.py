import requests
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from database.weather_dao import insert_weather_log
from services.alert_service import check_and_send_alerts

def map_wmo_code(code):
    """Maps WMO weather codes to string conditions."""
    if code == 0: return "Clear"
    if code in [1, 2, 3]: return "Clouds"
    if code in [45, 48]: return "Fog"
    if code in [51, 53, 55]: return "Drizzle"
    if code in [61, 63, 65, 80, 81, 82]: return "Rain"
    if code in [71, 73, 75, 77, 85, 86]: return "Snow"
    if code in [95, 96, 99]: return "Thunderstorm"
    return "Unknown"

def fetch_weather_for_city(city):
    """Fetches exact real-time weather data for a single city from Open-Meteo API."""
    try:
        # Step 1: Geocoding (City Name -> Lat, Lon)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            print(f"City not found in geocoding: {city}")
            return None
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        # Step 2: Weather Data (Lat, Lon -> Weather)
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,surface_pressure"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data["current_weather"]
        
        # Open-Meteo only gives current humidity/pressure inside 'hourly' arrays, so we take the first value
        humidity = weather_data["hourly"]["relative_humidity_2m"][0] if "hourly" in weather_data else 50
        pressure = weather_data["hourly"]["surface_pressure"][0] if "hourly" in weather_data else 1013
        
        return {
            "city": city,
            "temperature": current["temperature"],
            "humidity": humidity,
            "pressure": pressure,
            "weather_condition": map_wmo_code(current["weathercode"]),
            "wind_speed": current["windspeed"]
        }
    except Exception as e:
        print(f"Error fetching exact weather for {city}: {e}")
        return None

def fetch_all_cities():
    """Fetches data for all configured cities, saves to DB, and checks alerts."""
    results = []
    for city in config.CITIES:
        data = fetch_weather_for_city(city)
        if data:
            # Insert into database
            success = insert_weather_log(
                city=data['city'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                pressure=data['pressure'],
                weather_condition=data['weather_condition'],
                wind_speed=data['wind_speed']
            )
            if success:
                print(f"Successfully recorded weather for {city}.")
                # Check for alerts
                check_and_send_alerts(data)
            results.append(data)
    return results

def get_live_location_city():
    """Fetches the user's current city based on IP address."""
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            return data.get("city", "Unknown")
    except Exception as e:
        print(f"Error fetching live location: {e}")
    return "Unknown"

if __name__ == "__main__":
    fetch_all_cities()
