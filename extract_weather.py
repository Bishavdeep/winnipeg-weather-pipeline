import requests
import json
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LATITUDE = 49.8951
LONGITUDE = -97.1384
API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FWinnipeg"

def fetch_weather_data() -> dict:
    logging.info("Fetching weather data from Open-Meteo API...")
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        logging.info("Weather data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

def save_weather_data(data: dict, file_path: str) -> bool:
    logging.info(f"Saving weather data to {file_path}...")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info("Weather data saved successfully.")
        return True
    except IOError as e:
        logging.error(f"Error saving weather data: {e}")
        return False

def main():
    """Main Execution Function"""
    logging.info("Pipeline started.")

    #Step 1: Extract weather data
    weather_data = fetch_weather_data()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"raw_weather{timestamp}.json"

        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", file_name)

        save_weather_data(weather_data, filepath)   
    else:
        logging.warning("Failed to fetch weather data. Exiting pipeline.")

    logging.info("Pipeline completed.")

if __name__ == "__main__":
    main()