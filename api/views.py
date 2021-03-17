from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os
import json


class ApiWeatherView(APIView):

    def get(self, request):
        api_key = os.getenv("api_key")
        cnt="4"
        url = f"https://api.openweathermap.org/data/2.5/forecast?q=Warsaw,PL&appid={api_key}&cnt={cnt}"
        data = requests.get(url)
        with open("api/json.txt", "w") as outfile:
            json.dump(data.json(),outfile, indent=4)
        return Response(data.json())
