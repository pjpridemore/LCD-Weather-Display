from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import pytz

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")

CITY = "Knoxville"
lat = 35.962639
lon = -83.916718
five_day_URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"

# local timezone (Eastern Time)
local_tz = pytz.timezone("America/New_York")


def get_weather():
    # Request forecast data
    response = requests.get(five_day_URL)
    five_forecast_data = response.json()

    # Checking if API response is valid
    if "list" not in five_forecast_data:
        return None, None, None, None, "Error fetching data"

    # Get data for the current day
    current_data = five_forecast_data["list"][0]
    current_temp = round(current_data["main"]["temp"])
    icon_code = current_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

    # get the time in utc
    current_time_utc = datetime.now(pytz.UTC)
    # trim the time to the hour
    current_hour = int(current_time_utc.strftime("%H"))

    # determine if it's night
    is_night = current_hour >= 20 or current_hour < 7

    return (
        current_temp,
        icon_url,
        is_night,
    )


# getting the daily high and low from the 16 day api instead
cnt = 1
sixteen_day_URL = f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={API_KEY}&units=imperial"


def get_daily_high_and_low():
    # Request forecast data
    response2 = requests.get(sixteen_day_URL)
    sixteen_forecast_data = response2.json()

    # Checking if API response is valid
    if "list" not in sixteen_forecast_data:
        return None, None

    # daily highs and lows
    daily_data = sixteen_forecast_data["list"][0]
    daily_high = round(daily_data["temp"]["max"])
    daily_low = round(daily_data["temp"]["min"])

    # also getting the daily rain chance
    precip_chance = round(daily_data.get("pop", 0) * 100)

    return (daily_high, daily_low, precip_chance)


@app.route("/")
def home():
    current_temp, icon, is_night = get_weather()
    daily_high, daily_low, precip_chance = get_daily_high_and_low()

    return render_template(
        "index.html",
        temp=current_temp,
        high=daily_high,
        low=daily_low,
        precip=precip_chance,
        icon=icon,
        is_night=is_night,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
