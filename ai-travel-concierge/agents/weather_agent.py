import os
import requests

class WeatherAgent:
    def get_weather_info(self, destination, start_date, end_date=None):
        api_key = os.getenv("WEATHERAPI_API_KEY")
        if not api_key:
            return "WeatherAPI.com API key is missing."
        try:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={destination}&days=3"
            response = requests.get(url)
            data = response.json()
            if "forecast" not in data or "forecastday" not in data["forecast"]:
                return f"No weather data found for {destination}."
            result = []
            for day in data["forecast"]["forecastday"]:
                date = day.get("date", "N/A")
                condition = day.get("day", {}).get("condition", {}).get("text", "N/A")
                min_temp = day.get("day", {}).get("mintemp_c", "N/A")
                max_temp = day.get("day", {}).get("maxtemp_c", "N/A")
                result.append(f"{date}: {condition}, {min_temp}°C - {max_temp}°C")
            return "\n".join(result)
        except Exception as e:
            return f"Error retrieving weather data: {str(e)}"