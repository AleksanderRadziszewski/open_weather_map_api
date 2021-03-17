from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os


class ApiWeatherView(APIView):

    def get(self, request):
        latitude = "52.1347"
        longitude = "21.0042"
        api_key = os.getenv("api_key")
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={api_key}"
        data = requests.get(url)
        return Response(data.json())
