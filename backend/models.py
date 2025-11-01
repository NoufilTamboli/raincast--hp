# backend/models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from backend.database import Base
from datetime import datetime

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FloodAlert(Base):
    __tablename__ = "flood_alerts"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, nullable=False)
    alert_level = Column(String, nullable=False)
    predicted_rainfall = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
