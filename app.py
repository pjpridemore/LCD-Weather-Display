from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Knoxville"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"

def get_weather():
    response = requests.get(URL)
    data = response.json()
    temperature = round(data["main"]["temp"])
    high_temperature = round(data["main"]["temp_max"])
    low_temperature = round(data["main"]["temp_min"])
    description = data["weather"][0]["description"]


    rain = data.get("rain", {}).get("1h", 0)
    return temperature, high_temperature, low_temperature, rain, description

@app.route("/")
def home():
    temp, high, low, rain, desc = get_weather()
    return render_template("index.html", temp=temp, high=high, low=low, rain=rain, desc=desc)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
