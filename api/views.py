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
        list_dates = []
        data_requests = []
        list_objects = []
        for day in range(1, days + 1):
            forecast_date = now - timedelta(days=day)
            dt = int(datetime.timestamp(forecast_date))
            url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?" \
                  f"lat={lat}&lon={lon}&dt={dt}&units={units}&appid={api_key}"
            data_request = requests.get(url)
            data_requests.append(data_request.json())
        for day in data_requests:

            list_length = len(day["hourly"])
            for hour in range(list_length - 1):
                if day["hourly"][hour]["temp"] < day["hourly"][hour+1]["temp"]:
                    converted_temp_growth = datetime.fromtimestamp(day["hourly"][hour]["dt"])
                    list_dates.append(converted_temp_growth.isoformat())
                    list_objects.append(day["hourly"][hour])
        with open("api/json.txt", "w") as outfile:
            json.dump(list_objects, outfile, indent=4)
        with open("api/dates_and_hours.txt", "w") as dates_hours:
            for row in list_dates:
                dates_hours.write(str(row) + "\n")
        return Response(data_requests)
