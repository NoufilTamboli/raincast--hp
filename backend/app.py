from flask import Flask, jsonify, request
from database import engine, Base
from services.weather_service import fetch_and_store_weather

app = Flask(__name__)

Base.metadata.create_all(bind=engine)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Himachal Flood Prediction REST API"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "API is running"
    })


@app.route("/weather/fetch", methods=["GET"])
def fetch_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        weather = fetch_and_store_weather(city)

        return jsonify({
            "id": weather.id,
            "location_name": weather.location_name,
            "temperature": weather.temperature,
            "humidity": weather.humidity,
            "rainfall_mm": weather.rainfall_mm,
            "timestamp": weather.timestamp
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

