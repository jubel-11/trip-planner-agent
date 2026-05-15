"""
Weather Tool — fetches real weather using Open-Meteo (no API key needed).
Used to give packing tips and activity recommendations based on conditions.
"""

import requests


def get_weather(city: str) -> str:
    """
    Get current weather for a destination city.

    Args:
        city: Destination city name

    Returns:
        Weather summary with packing tips
    """
    try:
        # Geocode city
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10
        ).json()

        if not geo.get("results"):
            return f"Weather data not found for '{city}'. Pack for all conditions!"

        loc     = geo["results"][0]
        lat     = loc["latitude"]
        lon     = loc["longitude"]
        name    = f"{loc['name']}, {loc.get('country', '')}"

        # Fetch weather
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude":  lat,
                "longitude": lon,
                "current": [
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "weathercode",
                    "windspeed_10m",
                    "precipitation",
                ],
                "daily": ["temperature_2m_max", "temperature_2m_min",
                          "precipitation_sum"],
                "forecast_days": 3,
                "timezone": "auto",
            },
            timeout=10
        ).json()

        current = weather["current"]
        temp    = current["temperature_2m"]
        feels   = current["apparent_temperature"]
        humid   = current["relative_humidity_2m"]
        wind    = current["windspeed_10m"]

        wmo = {
            0: "Clear sky ☀️",  1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅", 3: "Overcast ☁️",
            45: "Foggy 🌫️",     61: "Rainy 🌧️",
            63: "Moderate rain 🌧️", 71: "Snowy ❄️",
            80: "Showers 🌦️",   95: "Thunderstorm ⛈️",
        }
        condition = wmo.get(current["weathercode"], "Variable conditions")

        # Packing tips based on temp
        if temp < 5:
            packing = "🧥 Pack heavy winter coat, gloves, thermal layers"
        elif temp < 15:
            packing = "🧣 Pack layers, jacket, light sweater"
        elif temp < 25:
            packing = "👕 Pack light layers, a jacket for evenings"
        else:
            packing = "🩴 Pack light clothes, sunscreen, hat"

        # Rain tip
        rain_tip = ""
        if current.get("precipitation", 0) > 0 or current["weathercode"] in [61, 63, 80]:
            rain_tip = "\n  ☂️  Bring an umbrella — rain expected."

        result = (
            f"Weather in {name}:\n"
            f"  🌡️  {temp}°C (feels like {feels}°C) | {condition}\n"
            f"  💧 Humidity: {humid}% | Wind: {wind} km/h\n"
            f"  👜 Packing tip: {packing}{rain_tip}"
        )
        return result

    except requests.exceptions.RequestException as e:
        return f"Network error fetching weather: {str(e)}"
    except Exception as e:
        return f"Weather error: {str(e)}"
