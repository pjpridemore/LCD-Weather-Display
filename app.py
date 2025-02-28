from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
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

# get today's date
current_date = datetime.now().date()

# format the day : Mon, Jan 01
pretty_date = current_date.strftime("%a, %b %d")


def get_weather():
    # request forecast data
    response = requests.get(five_day_URL)
    five_forecast_data = response.json()

    # checking if API response is valid
    if "list" not in five_forecast_data:
        return None, None, None, None, "Error fetching data"

    # get data for the current day
    current_data = five_forecast_data["list"][0]
    current_temp = round(current_data["main"]["temp"])
    feels_like = round(current_data["main"]["feels_like"])
    icon_code = current_data["weather"][0]["icon"]
    description = current_data["weather"][0]["description"].title()

    # get the current local time
    current_time_local = datetime.now(local_tz)

    # determine if it's daytime (6 AM to 6 PM)
    is_daytime = 6 <= current_time_local.hour < 18

    # override the icon code to use the day icon if it's daytime
    if is_daytime and icon_code.endswith("n"):
        icon_code = icon_code.replace("n", "d")

    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

    return (current_temp, icon_url, not is_daytime, feels_like, description)


def get_daily_high_and_low():
    cnt = 1
    sixteen_day_URL = f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={API_KEY}&units=imperial"

    # request forecast data
    response2 = requests.get(sixteen_day_URL)
    sixteen_forecast_data = response2.json()

    # checking if API response is valid
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
    current_temp, icon, is_night, feels_like, description = get_weather()
    daily_high, daily_low, precip_chance = get_daily_high_and_low()

    return render_template(
        "index.html",
        temp=current_temp,
        feels_like=feels_like,
        high=daily_high,
        low=daily_low,
        precip=precip_chance,
        icon=icon,
        is_night=is_night,
        description=description,
        pretty_date=pretty_date,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
