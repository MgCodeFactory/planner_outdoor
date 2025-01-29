from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from meteofrance_api import MeteoFranceClient
from rest_framework import status, response
from datetime import datetime
import requests
import os
import logging

weather_client = MeteoFranceClient()
logger = logging.getLogger(__name__)


class CustomConvertion():
    """
    Custom conversion class data.
    """

    # convert timestamp in YYYY-MM-DD
    def convert_timestamp(self, timestamp):
        """
        Convert timestamp to date.
        """
        dt_object = datetime.fromtimestamp(timestamp)
        converted_date = {
            "year": dt_object.strftime("%Y"),
            "month": dt_object.strftime("%B"),
            "day": dt_object.strftime("%d")
        }
        return converted_date

    def convert_temp_in_farhenheit(self, temp_in_celsius):
        """
        Convert temperature from Celsius to Fahrenheit.
        """
        return round((temp_in_celsius * 9/5) + 32, 1)

    def convert_wind_speed(self, wind_speed):
        """
        Convert wind speed from m/s to km/h.
        """
        return round(wind_speed * 3.6, 2)

    def convert_wind_direction(self, wind_direction):
        """
        Convert wind direction from degrees to cardinal direction.
        """
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(wind_direction / 45) % 8
        return directions[index]


class GeocodingView(GenericAPIView):
    """
    Retreive geographic coordinates.
    Using Openweathermap Geocoding API.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Get coordinates from city name.
        """
        city = kwargs.get("city")
        limit = 10
        api_key = os.environ.get("OWM_API_KEY")
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={
            city}&limit={limit}&appid={api_key}"

        try:
            api_response = requests.get(geocoding_url)
            api_response.raise_for_status()
            data = api_response.json()
            if data:
                output_data = []
                for item in data:
                    output_data.append(
                        {
                            "name": item["name"],
                            "lat": item["lat"],
                            "lon": item["lon"],
                            "country": item["country"],
                        }
                    )
                return response.Response({"data": output_data}, status=status.HTTP_200_OK)
            else:
                return response.Response({"error": "City not found."}, status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            return response.Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherView(GenericAPIView):
    """
    Retreive weather data.
    Using Meteofrance API.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Get weather data from coordinates.
        """
        lat = float(kwargs.get("lat"))
        lon = float(kwargs.get("lon"))
        try:
            weather_data = weather_client.get_forecast(
                latitude=lat, longitude=lon, language="en"
            )
            daily_weather_data = weather_data.daily_forecast[:15]
            url_icon = "https://meteofrance.com/modules/custom/mf_tools_common_theme_public/svg/weather"

            final_data = []
            for day in daily_weather_data:
                final_data.append(
                    {
                        "date": CustomConvertion().convert_timestamp(day["dt"]),
                        "weather": day["weather12H"]["desc"],
                        "weather_icon": day["weather12H"]["icon"],
                        "temperature": {
                            "min_C": day["T"]["min"],
                            "max_C": day["T"]["max"],
                            "min_F": CustomConvertion().convert_temp_in_farhenheit(
                                day["T"]["min"]
                            ),
                            "max_F": CustomConvertion().convert_temp_in_farhenheit(
                                day["T"]["max"]
                            ),
                        },
                    }
                )
            return response.Response(
                {"data": final_data, "url_icon": url_icon}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
