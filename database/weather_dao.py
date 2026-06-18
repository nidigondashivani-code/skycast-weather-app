from sqlalchemy import func
from database.models import WeatherLog, User
from database.db_connection import get_session

def insert_weather_log(city, temperature, humidity, pressure, weather_condition, wind_speed):
    """Inserts a new weather record into the database."""
    session = get_session()
    try:
        log = WeatherLog(
            city=city,
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            weather_condition=weather_condition,
            wind_speed=wind_speed
        )
        session.add(log)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error inserting weather log: {e}")
        return False
    finally:
        session.close()

def get_weather_history(city=None):
    """Returns weather history for a specific city or all cities."""
    session = get_session()
    try:
        query = session.query(WeatherLog)
        if city:
            query = query.filter(WeatherLog.city == city)
        return query.order_by(WeatherLog.fetched_time.desc()).all()
    finally:
        session.close()

def get_top_hottest_cities():
    """Returns a list of cities and their maximum recorded temperature."""
    session = get_session()
    try:
        return session.query(
            WeatherLog.city, 
            func.max(WeatherLog.temperature).label('max_temp')
        ).group_by(WeatherLog.city).all()
    finally:
        session.close()

def get_average_temperature():
    """Returns the average temperature across all records."""
    session = get_session()
    try:
        result = session.query(func.avg(WeatherLog.temperature)).scalar()
        return round(result, 2) if result else None
    finally:
        session.close()
