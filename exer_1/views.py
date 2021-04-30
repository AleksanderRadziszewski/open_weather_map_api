from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os
import json
from datetime import timedelta, datetime


# Przedziały czasowe gdzie odnotowuje się ciągły wzrost temperatury


class ApiTempGrowthView(APIView):

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
        # Wysyłamy zapytanie o prognoze pogody dla trzech dni poprzedzających dzień dzisiejszy
        for day in range(1, days + 1):
            forecast_date = now - timedelta(days=day)
            dt = int(datetime.timestamp(forecast_date))
            url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?" \
                  f"lat={lat}&lon={lon}&dt={dt}&units={units}&appid={api_key}"
            data_request = requests.get(url)
            data_requests.append(data_request.json())
        # obsługujemy każdy dzień
        for day in data_requests:
            list_length = len(day["hourly"])
            local = []
            item = day["hourly"]

            for hour in range(1, list_length):
                # stawiamy warunek by spr czy następuje wzrost temp dla konkretnej godziny
                if item[hour - 1]["temp"] < item[hour]["temp"]:
                    local.append(item[hour - 1])
                    timestamp_1 = local[-1]["dt"]
                    timestamp_2 = item[hour]["dt"]
                    time_1 = datetime.fromtimestamp(timestamp_1)
                    time_2 = datetime.fromtimestamp(timestamp_2)
                    try:
                        # sprawdzamy ostatni punkt przedzialu gdzie wzrasta temp i zapisujemy go
                        if time_2 == time_1 + delta and item[hour + 1]["temp"] < item[hour]["temp"]:
                            local.append(item[hour])
                            local_2 = local.copy()
                            list_objects.append(local_2)
                            local.clear()
                    except IndexError:
                        pass
        # czas rozpoczęcia, czas trwania, temp początkowa i temp końcowa
        for last in list_objects:
            time_start = datetime.fromtimestamp(last[0]["dt"])
            time_end = datetime.fromtimestamp(last[-1]["dt"])
            duration = time_end - time_start
            duration_seconds = int(duration.total_seconds())
            secs_in_a_hour = 3600
            hours, seconds = divmod(duration_seconds, secs_in_a_hour)

            data = {"start_time_growth": time_start.isoformat(),  # czas rozpoczęcia wzrostu
                    "duration_of_growth": f"{hours} hours",  # czas trwania wzrostu w godzinach
                    "initial_temp": f"{last[0]['temp']} C",  # temperatura początkowa
                    "end_temp": f"{last[-1]['temp']} C"}  # temperatura końcowa

            last.insert(0, data)

        # wrzucamy dane do pliku data.json
        with open("data.json", "w") as outfile:
            json.dump(list_objects, outfile, indent=4)
        return Response(list_objects)
