from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherLog(Base):
    __tablename__ = 'weather_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    weather_condition = Column(String(100), nullable=False)
    wind_speed = Column(Float, nullable=False)
    fetched_time = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
