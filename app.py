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
URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"

# local timezone (Eastern Time)
local_tz = pytz.timezone("America/New_York")


def get_weather():
    # Request forecast data
    response = requests.get(URL)
    forecast_data = response.json()

    # Checking if API response is valid
    if "list" not in forecast_data:
        return None, None, None, None, "Error fetching data"

    # Get data for the current day
    current_data = forecast_data["list"][0]
    current_temp = round(current_data["main"]["temp"])
    current_high = round(current_data["main"]["temp_max"])
    current_low = round(current_data["main"]["temp_min"])
    icon_code = current_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
    current_precip_chance = round(current_data.get("pop", 0) * 100)

    # get sunset time (convert from UTC to local)
    sunset_utc = forecast_data["city"]["sunset"]
    sunset_time = datetime.fromtimestamp(sunset_utc, tz=timezone.utc).astimezone(
        local_tz
    )
    print("Sunset time is: ")
    print(sunset_time)

    # get current time
    current_time = datetime.now(tz=local_tz)
    print("current time is: ")
    print(current_time)

    # determine if it's night
    is_night = current_time >= sunset_time

    print("Is it night?", is_night)

    return (
        current_temp,
        current_high,
        current_low,
        current_precip_chance,
        icon_url,
        is_night,
    )


@app.route("/")
def home():
    current_temp, high_temp, low_temp, current_precip_chance, icon, is_night = (
        get_weather()
    )
    return render_template(
        "index.html",
        temp=current_temp,
        high=high_temp,
        low=low_temp,
        precip=current_precip_chance,
        icon=icon,
        is_night=is_night,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
