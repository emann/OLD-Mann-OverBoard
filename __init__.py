from flask import Flask, flash, redirect, render_template, request, session, abort
import requests
from datetime import datetime, timedelta
import threading
import config

app = Flask(__name__)
threads = []


@app.route("/")
def index():
    return render_template("index.html", current_conditions=get_current_weather(),
                           forecast=get_forecast_weather(), timestuff=get_time_stuff())

def get_time_stuff():
    today = datetime.now()
    timestuff = [(today.strftime('%A'), today.strftime('%B %d'))]
    for i in range(1, 5):
        day = today+timedelta(days=i)
        timestuff.append((day.strftime('%A'), day.day))

    return timestuff

def get_current_weather():
    response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/2217809?apikey={config.API_KEYS['accuweather']}")
    unformatted_current = response.json()[0]
    current_conditions = {
        "temp": int(unformatted_current["Temperature"]["Imperial"]["Value"]),
        "weather_icon": f"https://developer.accuweather.com/sites/default/files/{unformatted_current['WeatherIcon']:02d}-s.png",
    }
    return current_conditions


def get_forecast_weather():
    response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/2217809?apikey={config.API_KEYS['accuweather']}")
    unformatted_forecasts = response.json()["DailyForecasts"]
    forecasts = []
    for day in unformatted_forecasts:
        formatted_forecast = {
            "weekday": datetime.fromtimestamp(day["EpochDate"]).strftime("%A"),
            "temp_min": int(day["Temperature"]["Minimum"]["Value"]),
            "temp_max": int(day["Temperature"]["Maximum"]["Value"]),
            "weather_icon": f"https://developer.accuweather.com/sites/default/files/{day['Day']['Icon']:02d}-s.png",
        }
        forecasts.append(formatted_forecast)
    return forecasts


def update_weather():
    pass


def update_calendar():
    pass


def start_threads():
    threads.append(threading.Thread(target=update_weather, daemon=True))  # Updating current conditions and forecast displays
    threads.append(threading.Thread(target=update_calendar, daemon=True)) # Updating calendar display information
    for t in threads:
        t.start()


if __name__ == "__main__":
    start_threads()
    app.run(host='0.0.0.0', port=80)