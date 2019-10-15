import requests
import datetime.datetime
import threading
from time import sleep
from todoist import TodoistAPI


class TodoistInterface:

    def __init__(self, api_key, project_id=None, num_days=7):
        self.api_key = api_key
        self.api = TodoistAPI(self.api_key)
        self.project_id = project_id
        self.num_days = num_days

    def filter(self, item):
        if self.project_id:
            return item['project_id'] == self.project_id and not item['parent_id']
        else:
            return not item['parent_id']

    def get_task_tuples(self): ##ToDo: Sort tuples by date
        unsorted_tuples = [(item['content'], item['due']['date'] for item in self.api.items.all(filt=self.filter)]
        return unsorted_tuples


class AccuWeatherInterface:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self):
        response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/2217809?apikey={self.api_key}")
        unformatted_current = response.json()[0]
        current_conditions = {
            "temp": int(unformatted_current["Temperature"]["Imperial"]["Value"]),
            "weather_icon": f"https://developer.accuweather.com/sites/default/files/{unformatted_current['WeatherIcon']:02d}-s.png",
        }
        return current_conditions

    def get_forecast_weather(self):
        response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/2217809?apikey={self.api_key}")
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


class GoogleCalendarInterface:
    def __init__(self, api_key):
        self.api_key = api_key


class InterfaceManager:
    def __init__(self, api_key_dict: dict, settings: dict):
        self.todoist_interface = TodoistInterface(api_key=api_key_dict['todoist'])
        self.accweather_interface = AccuWeatherInterface(api_key=api_key_dict['accuweather'])
        self.google_calendar_interface = TodoistInterface(api_key=api_key_dict['todoist'])

        self.update_interval = 300

        self.data = {}
        self.auto_update = False
        self.force_update()

    def start_updates(self):
        self.auto_update = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def stop_updates(self):
        self.auto_update = False

    def force_update(self):
        self.data = {
            'weather': self.accweather_interface.get_weather(),
            'todoist': self.todoist_interface.get_task_tuples(),
            'calendar': self.google_calendar_interface.get_calendar_events()
        }

    def update_loop(self):
        while self.auto_update:
            self.force_update()
            sleep(self.update_interval)
