from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os
import json
from datetime import timedelta


class ApiWeatherView(APIView):

    def get(self, request):
        api_key = os.getenv("api_key")
        lat = "52.1356"
        lon = "21.0030"
        units = "imperial"
        now = datetime.now()
        days = 3
        list_dates_start = []
        list_dates_end = []
        data_requests = []
        list_objects = []
        for day in range(1,days+1):
            forecast_date = now - timedelta(days=day)
            dt = int(datetime.timestamp(forecast_date))
            url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?" \
                  f"lat={lat}&lon={lon}&dt={dt}&units={units}&appid={api_key}"
            data_request = requests.get(url)
            data_requests.append(data_request.json())

        for day in data_requests:
            list_length = len(day["hourly"])
            index = 0
            for hour in range(1, list_length):
                if day["hourly"][hour-1]["temp"] <= day["hourly"][hour]["temp"]:
                    list_dates_start.append(day["hourly"][hour]["temp"])
                    list_objects.append(day["hourly"][hour]["temp"])
                    index = hour
            if day["hourly"][index+1]["temp"] < day["hourly"][index]["temp"]:
                list_dates_end.append(day["hourly"][index]["temp"])
        with open("api/json.txt", "w") as outfile:
            json.dump(list_objects, outfile, indent=4)
        with open("api/dates_and_hours.txt", "w") as dates_hours:
            for row in list_dates_start:
                dates_hours.write(str(row) + "\n")
        return Response(data_requests)
