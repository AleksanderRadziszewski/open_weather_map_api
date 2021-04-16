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
            local = []
            item = day["hourly"]

            for hour in range(1, list_length):
                if item[hour - 1]["temp"] < item[hour]["temp"]:
                    local.append(item[hour - 1])
                    timestamp_1 = local[-1]["dt"]
                    timestamp_2 = item[hour]["dt"]
                    time_1 = datetime.fromtimestamp(timestamp_1)
                    time_2 = datetime.fromtimestamp(timestamp_2)
                    try:
                        if time_2 == time_1 + delta and item[hour + 1]["temp"] < item[hour]["temp"]:
                            local.append(item[hour])
                            local_2 = local.copy()
                            list_objects.append(local_2)
                            local.clear()
                    except IndexError:
                        pass
        for last in list_objects:
            time_start = datetime.fromtimestamp(last[0]["dt"])
            time_end = datetime.fromtimestamp(last[-1]["dt"])
            duration = time_end - time_start
            duration_seconds = int(duration.total_seconds())
            secs_in_a_hour = 3600
            hours, seconds = divmod(duration_seconds, secs_in_a_hour)
            data = {"start_time_growth": time_start.isoformat(),
                    "duration_of_growth": f"{hours} hours",
                    "end_time_growth": time_end.isoformat()}
            last.insert(0, data)
        with open("api/json.txt", "w") as outfile:
            json.dump(list_objects, outfile, indent=4)
        return Response(list_objects)
