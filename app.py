from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Knoxville"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"

def get_weather():
    response = requests.get(URL)
    data = response.json()
    temperature = data["main"]["temp"]
    high_temperature = data["main"]["temp_max"]
    low_temperature = data["main"]["temp_min"]

    rain = data.get("rain", {}).get("1h", 0)
    return temperature, high_temperature, low_temperature, rain

@app.route("/")
def home():
    temp, high, low, rain = get_weather()
    return render_template_string("""
        <h1>Knoxville, TN</h1>
        <h2>Temperature: {{ temp }}°F</h2>
        <h2>High:{{ high }} Low: {{ low }}</h2>
        <h2>Rain: {{ rain}} mm</h2>
    """, temp=temp,high = high, low = low, rain=rain)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
