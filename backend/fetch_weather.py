import os
import requests
from dotenv import load_dotenv
from backend.database import SessionLocal
from backend.models import WeatherData
from datetime import datetime

# Load .env variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        print(f"❌ Failed for {city_name}: {data}")
        return None

    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    rainfall = data.get('rain', {}).get('1h', 0.0)

    db = SessionLocal()
    entry = WeatherData(
        location_name=city_name,
        temperature=temperature,
        humidity=humidity,
        rainfall_mm=rainfall,
        timestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()
    db.close()
    print(f"✅ Saved weather data for {city_name}")

# Example usage
if __name__ == "__main__":
    cities = ["Shimla", "Mandi", "Kullu", "Kangra"]
    for city in cities:
        fetch_weather(city)
