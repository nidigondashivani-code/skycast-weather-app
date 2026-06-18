import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.weather_dao import get_weather_history

def generate_weather_report(city=None, filename="weather_report.csv"):
    """Generates a CSV report from the database weather history."""
    logs = get_weather_history(city)
    
    if not logs:
        print("No data available to generate report.")
        return None
        
    data = [{
        "City": log.city,
        "Temperature (C)": log.temperature,
        "Humidity (%)": log.humidity,
        "Pressure (hPa)": log.pressure,
        "Condition": log.weather_condition,
        "Wind Speed (m/s)": log.wind_speed,
        "Time Recorded": log.fetched_time.strftime("%Y-%m-%d %H:%M:%S")
    } for log in logs]
    
    df = pd.DataFrame(data)
    
    # Ensure reports directory exists
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, filename)
    df.to_csv(filepath, index=False)
    
    print(f"Report successfully generated at {filepath}")
    return filepath
