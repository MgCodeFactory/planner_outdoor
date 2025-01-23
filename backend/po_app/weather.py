import requests
from rest_framework import status, response
from rest_framework.generics import GenericAPIView
import os
from rest_framework.permissions import AllowAny


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
                            "state": item["state"],
                        }
                    )
                return response.Response({"data": output_data}, status=status.HTTP_200_OK)
            else:
                return {"error": "City not found."}, status.HTTP_404_NOT_FOUND
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
