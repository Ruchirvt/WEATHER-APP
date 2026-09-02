"""
Thin wrapper around the OpenWeatherMap free-tier APIs:
  - Current Weather Data API
  - 5 Day / 3 Hour Forecast API (used to build the 3-day outlook)

All functions return plain dicts/DataFrames so the rest of the app
doesn't need to know anything about OpenWeatherMap's response shape.
"""

import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPIError(Exception):
    pass


def get_current_weather(lat: float, lon: float, api_key: str) -> dict:
    """Fetch live current weather for a coordinate."""
    url = f"{BASE_URL}/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        raise WeatherAPIError(resp.json().get("message", "Failed to fetch current weather"))
    data = resp.json()

    return {
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "wind_deg": data["wind"].get("deg", 0),
        "clouds": data["clouds"]["all"],
        "rain_1h": data.get("rain", {}).get("1h", 0.0),
        "visibility": data.get("visibility", 10000),
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
        "observed_at": datetime.fromtimestamp(data["dt"]),
        "city": data.get("name", ""),
    }


def get_forecast_raw(lat: float, lon: float, api_key: str) -> list:
    """Fetch the raw 5-day/3-hour forecast list (40 entries)."""
    url = f"{BASE_URL}/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        raise WeatherAPIError(resp.json().get("message", "Failed to fetch forecast"))
    return resp.json()["list"]


def get_forecast_dataframe(lat: float, lon: float, api_key: str) -> pd.DataFrame:
    """Return the full 3-hourly forecast as a tidy DataFrame (for charts)."""
    raw = get_forecast_raw(lat, lon, api_key)
    rows = []
    for entry in raw:
        rows.append({
            "datetime": datetime.fromtimestamp(entry["dt"]),
            "temp": entry["main"]["temp"],
            "feels_like": entry["main"]["feels_like"],
            "humidity": entry["main"]["humidity"],
            "pressure": entry["main"]["pressure"],
            "wind_speed": entry["wind"]["speed"],
            "rain_3h": entry.get("rain", {}).get("3h", 0.0),
            "clouds": entry["clouds"]["all"],
            "condition": entry["weather"][0]["main"],
            "description": entry["weather"][0]["description"],
            "pop": entry.get("pop", 0.0) * 100,  # probability of precipitation, as %
        })
    return pd.DataFrame(rows)


def get_3day_summary(lat: float, lon: float, api_key: str) -> pd.DataFrame:
    """
    Collapse the 3-hourly forecast into a daily summary for the next 3 days:
    avg/min/max temp, total rain, max wind, avg humidity, dominant condition.
    """
    df = get_forecast_dataframe(lat, lon, api_key)
    df["date"] = df["datetime"].dt.date

    daily = df.groupby("date").agg(
        temp_avg=("temp", "mean"),
        temp_min=("temp", "min"),
        temp_max=("temp", "max"),
        humidity_avg=("humidity", "mean"),
        pressure_avg=("pressure", "mean"),
        wind_max=("wind_speed", "max"),
        rain_total=("rain_3h", "sum"),
        pop_max=("pop", "max"),
    ).reset_index()

    # Dominant weather condition per day (most frequent)
    dominant = df.groupby("date")["condition"].agg(lambda x: x.value_counts().idxmax())
    daily["condition"] = daily["date"].map(dominant)

    return daily.head(3)
