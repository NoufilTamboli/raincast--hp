# backend/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import WeatherData
from datetime import datetime

# Create a router object
router = APIRouter()

# ✅ Route: Add weather data
@router.post("/add-weather")
def add_weather(location_name: str, temperature: float, humidity: float, rainfall_mm: float, db: Session = Depends(get_db)):
    entry = WeatherData(
        location_name=location_name,
        temperature=temperature,
        humidity=humidity,
        rainfall_mm=rainfall_mm,
        timestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"message": "✅ Weather data saved", "id": entry.id}

# ✅ Route: Get all weather records
@router.get("/weather")
def get_weather(db: Session = Depends(get_db)):
    data = db.query(WeatherData).all()
    return data
