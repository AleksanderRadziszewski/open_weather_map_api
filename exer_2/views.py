import json
from datetime import datetime
import statistics
from rest_framework.views import APIView
from rest_framework.response import Response


class ApiTempStepView(APIView):

    def get(self, request):

        temperature_jumps = []

        with open('data.json', 'r') as json_data:
            list_objects = json.load(json_data)

        for last in list_objects:
            humidity_data = [last[humidity_hour]["humidity"] for humidity_hour in range(1, len(last))]
            pressure_data = [last[pressure_hour]["pressure"] for pressure_hour in range(1, len(last))]
            humidity_avg = round(statistics.mean(humidity_data), 2)
            pressure_avg = round(statistics.mean(pressure_data), 2)


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
                         "value_of_step_one_hour": current_max_value[2],
                         "humidity_avg": humidity_avg,
                         "pressure_avg": pressure_avg}
            list_objects.insert(0, data_step)

            return Response(list_objects)
