from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os
import json


class ApiWeatherView(APIView):

    def get(self, request):
        api_key = os.getenv("api_key")
        lat="33.441792"
        lon="-94.037689"
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=daily,current,minutely,alerts&units=metric&appid={api_key}"
        data = requests.get(url)
        with open("api/json.txt", "w") as outfile:
            json.dump(data.json(),outfile, indent=4)
        return Response(data.json())
