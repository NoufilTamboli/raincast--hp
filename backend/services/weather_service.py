import requests
import os
from dotenv import load_dotenv
from database import SessionLocal
from models import WeatherData

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_and_store_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception(data.get("message", "Failed to fetch weather"))

    rainfall = 0
    if "rain" in data and "1h" in data["rain"]:
        rainfall = data["rain"]["1h"]

    weather_record = WeatherData(
        location_name=city,
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        rainfall_mm=rainfall
    )

    db = SessionLocal()
    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)
    db.close()

    return weather_record
