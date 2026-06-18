import schedule
import time
import threading
from database.db_connection import init_db
from services.weather_service import fetch_all_cities

def run_scheduler():
    print("Starting Background Weather Monitor...")
    # Fetch immediately on start
    fetch_all_cities()
    
    # Schedule to run every 1 hour
    schedule.every(1).hours.do(fetch_all_cities)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    init_db()
    run_scheduler()
