from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os
import json
from datetime import timedelta, datetime



class ApiWeatherView(APIView):

    def get(self, request):
        api_key = os.getenv("api_key")
        lat = "52.1356"
        lon = "21.0030"
        units = "imperial"
        now = datetime.now()
        days = 3
        delta = timedelta(hours=1)
        list_start = []
        list_end = []
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
            local_start = []
            local_end = []
            item = day["hourly"]
            for hour in range(1, list_length):
                if item[hour - 1]["temp"] < item[hour]["temp"]:
                    local_start.append(item[hour - 1])
                    local_end.append(item[hour])
            local_start.append(local_end[-1])
            list_start.append(local_start)
            list_end.append(local_end)

        for filter_temp in list_start:
            local_filter = []

            for dt in range(1,len(filter_temp)):
                timestamp_1 = filter_temp[dt - 1]["dt"]
                timestamp_2 = filter_temp[dt]["dt"]
                time_1 = datetime.fromtimestamp(timestamp_1)
                time_2 = datetime.fromtimestamp(timestamp_2)
                if time_2 == time_1 + delta:
                    local_filter.append(filter_temp[dt])
            list_objects.append(local_filter)
        with open("api/json.txt", "w") as outfile:
            json.dump(list_objects, outfile, indent=4)
        with open("api/dates_and_hours.txt", "w") as dates_hours:
            for row in list_start:
                dates_hours.write(str(row) + "\n")
        return Response(list_objects)
