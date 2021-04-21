from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os
import json
import statistics
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
        temperature_jumps = []
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
            humidity_data = [last[humidity_hour]["humidity"] for humidity_hour in range(1, len(last))]
            pressure_data = [last[pressure_hour]["pressure"] for pressure_hour in range(1, len(last))]
            humidity_avg = round(statistics.mean(humidity_data),2)
            pressure_avg = round(statistics.mean(pressure_data),2)
            data = {"start_time_growth": time_start.isoformat(),
                    "duration_of_growth": f"{hours} hours",
                    "end_time_growth": time_end.isoformat(),
                    "humidity_avg": humidity_avg,
                    "pressure_avg": pressure_avg}
            last.insert(0, data)
            for step in range(2, len(last)):
                biggest_distinction_last = round(max([last[step]["temp"] - last[step - 1]["temp"]]), 2)
                if biggest_distinction_last:
                    biggest_value_date_last = datetime.fromtimestamp(last[step]["dt"]).isoformat()
                    lowest_value_date_last = datetime.fromtimestamp(last[step - 1]["dt"]).isoformat()
                    temperature_jumps.append(
                        (lowest_value_date_last, biggest_value_date_last, biggest_distinction_last))

        current_max_value = None
        for s, e, v in temperature_jumps:
            if current_max_value is not None:
                if v >= current_max_value[2]:
                    current_max_value = (s, e, v)
            else:
                current_max_value = (s, e, v)

        data_step = {"beginning_time_biggest_step": current_max_value[0],
                     "ending_time_biggest_step": current_max_value[1],
                     "value_of_step_one_hour": current_max_value[2]}
        list_objects.insert(0, data_step)

        with open("api/json.txt", "w") as outfile:
            json.dump(list_objects, outfile, indent=4)
        return Response(list_objects)
