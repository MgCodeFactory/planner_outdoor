from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from meteofrance_api import MeteoFranceClient
from rest_framework import status, response
from datetime import datetime
import requests
import os

import logging

logger = logging.getLogger(__name__)

weather_client = MeteoFranceClient()


class CustomConvertion():
    """
    Custom conversion class data.
    """

    def convert_datetime(self, locale_datetime):
        """
        Convert datetime.
        """
        dt_object = datetime.fromisoformat(locale_datetime)
        converted_date = {
            "date": dt_object.strftime("%Y-%m-%d"),
            "year": dt_object.strftime("%Y"),
            "month": dt_object.strftime("%m"),
            "day": dt_object.strftime("%d"),
            "hour": dt_object.strftime("%H:%M")
        }
        return converted_date

    def convert_temp_in_farhenheit(self, temp_in_celsius):
        """
        Convert temperature from Celsius to Fahrenheit.
        """
        return round((temp_in_celsius * 9/5) + 32, 1)

    def convert_wind_speed(self, speed):
        """c
        Convert wind speed from km/h to mph.
        """
        return round(speed * 0.621371, 2)

    def convert_wind_direction(self, direction):
        """
        Convert wind direction from degrees to cardinal direction.
        """
        if direction == -1:
            return "Variable"
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(direction / 45) % 8
        return directions[index]

    def convert_meters_to_feet(self, meters):
        """
        Convert meters to feet.
        """
        return round(meters * 3.28084, 2)


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
            for index, day in enumerate(daily_weather_data):
                locale_datetime = str(weather_data.timestamp_to_locale_time(
                    day["dt"]))
                converted_datetime = CustomConvertion().convert_datetime(
                    locale_datetime)

                final_data.append(
                    {
                        "day_id": index,
                        "date": converted_datetime["date"],
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
                        }
                    }
                )
            return response.Response(
                {"data": final_data, "url_icon": url_icon}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherDetailsView(GenericAPIView):
    """
    Retreive weather data details.
    Using Meteofrance API.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Get weather data details from coordinates.
        """
        lat = float(kwargs.get("lat"))
        lon = float(kwargs.get("lon"))
        day_id = int(kwargs.get("day_id"))
        try:
            weather_data = weather_client.get_forecast(
                latitude=lat, longitude=lon, language="en"
            )

            if day_id < 0 or day_id >= len(weather_data.forecast):
                return response.Response({"error": "Invalid day ID"}, status=status.HTTP_400_BAD_REQUEST)

            selected_day = weather_data.daily_forecast[day_id]
            selected_day_details = weather_data.forecast[day_id]
            url_icon = "https://meteofrance.com/modules/custom/mf_tools_common_theme_public/svg/weather"

            locale_datetime = str(weather_data.timestamp_to_locale_time(
                selected_day["dt"]))
            converted_datetime = CustomConvertion().convert_datetime(
                locale_datetime)
            locale_sunrise = str(weather_data.timestamp_to_locale_time(
                selected_day["sun"]["rise"]))
            converted_sunrise = CustomConvertion().convert_datetime(locale_sunrise)
            locale_sunset = str(weather_data.timestamp_to_locale_time(
                selected_day["sun"]["set"]))
            converted_sunset = CustomConvertion().convert_datetime(locale_sunset)

            final_detailled_data = {
                "date": converted_datetime["date"],
                "weather": selected_day["weather12H"]["desc"],
                "weather_icon": selected_day["weather12H"]["icon"],
                "temperature": {
                    "min_C": selected_day["T"]["min"],
                    "max_C": selected_day["T"]["max"],
                    "min_F": CustomConvertion().convert_temp_in_farhenheit(
                        selected_day["T"]["min"]
                    ),
                    "max_F": CustomConvertion().convert_temp_in_farhenheit(
                        selected_day["T"]["max"]
                    )
                },
                "humidity": {"min": selected_day["humidity"]["min"], "max": selected_day["humidity"]["max"]},
                "uv": selected_day["uv"],
                "sunrise": converted_sunrise["hour"],
                "sunset": converted_sunset["hour"],
                "sea_level": selected_day_details["sea_level"],
                "wind": {
                    "speed_kmh": selected_day_details["wind"]["speed"],
                    "speed_mph": CustomConvertion().convert_wind_speed(selected_day_details["wind"]["speed"]),
                    "direction": CustomConvertion().convert_wind_direction(selected_day_details["wind"]["direction"])
                },
                "rain": selected_day_details.get("rain", {}).get("6h"),
                "iso0": {
                    "meters": selected_day_details["iso0"],
                    "feet": CustomConvertion().convert_meters_to_feet(selected_day_details["iso0"])
                }
            }
            return response.Response(
                {"data": final_detailled_data, "url_icon": url_icon}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
