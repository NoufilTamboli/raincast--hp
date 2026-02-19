# backend/auto_fetch.py
import time
from datetime import datetime
from backend.fetch_weather import fetch_weather, CITIES


# How often to fetch data (in minutes)
INTERVAL_MINUTES = 1  # 1 hour; change to 5 for testing

def fetch_all_cities():
    print(f"\n[{datetime.utcnow()}] 🔄 Starting fetch cycle...")
    for city in CITIES:
        try:
            fetch_weather(city)
        except Exception as e:
            print(f"❌ Error while fetching {city}: {e}")
    print(f"[{datetime.utcnow()}] ✅ Fetch cycle finished.\n")

if __name__ == "__main__":
    while True:
        fetch_all_cities()
        print(f"⏳ Sleeping for {INTERVAL_MINUTES} minutes...\n")
        time.sleep(INTERVAL_MINUTES * 60)
