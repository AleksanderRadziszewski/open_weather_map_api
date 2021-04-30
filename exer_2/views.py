import json
from datetime import datetime
import statistics
from rest_framework.views import APIView
from rest_framework.response import Response


class ApiTempStepView(APIView):

    def get(self, request):

        temperature_jumps_one_hour = []
        temperature_growth_period = []
        lowest_value_temp_max_step = 0
        humidity_avg = 0
        pressure_avg = 0

        # wczytujemy dane z pliku data.json i przypisujemy je do zmiennej list_objects

        with open('data.json', 'r') as json_data:
            list_objects = json.load(json_data)

        for last in list_objects:

            for step in range(2, len(last)):
                biggest_distinction_last = round(max([last[step]["temp"] - last[step - 1]["temp"]]), 2)
                #  sprawdzamy gdzie był największy skok temp w przeciągu godziny
                if biggest_distinction_last:
                    lowest_value_date_last = datetime.fromtimestamp(last[step - 1]["dt"]).isoformat()
                    lowest_value_temp_max_step = last[step]["temp"]
                    temperature_jumps_one_hour.append(
                        (lowest_value_date_last, biggest_distinction_last))
                    # konwertuejmy czas na czas w formacie ISO 8601
                    time_initial = datetime.fromtimestamp(last[1]["dt"]).isoformat()
                    time_end = datetime.fromtimestamp(last[-1]["dt"]).isoformat()
                    temperature_growth_period.append((time_initial, time_end))
                    # tworzymy listę wartości wilgotności oraz listę wartości ciśnienia dla poszczególnych pomiarów
                    humidity_data = [last[humidity_hour]["humidity"] for humidity_hour in range(1, len(last))]
                    pressure_data = [last[pressure_hour]["pressure"] for pressure_hour in range(1, len(last))]
                    # wyliczamy średnią wartość wilgotności i ciśneinia dla okresu wzrostu temp
                    humidity_avg = round(statistics.mean(humidity_data), 2)
                    pressure_avg = round(statistics.mean(pressure_data), 2)

            # temperatura poprzeddnia i maksymalny skok temp
            current_max_value = None
            for s, v in temperature_jumps_one_hour:
                if current_max_value is not None:
                    if v >= current_max_value[1]:
                        current_max_value = (s, v)
                else:
                    current_max_value = (s, v)

            data_step = {"beginning_period": f"{temperature_growth_period[0][0]}",
                         # początek okresu kiedy nastąpił największy skok
                         "end_period": f"{temperature_growth_period[0][1]}",
                         # koniec okresu kiedy nastąpił największy skok
                         "lowest_value_max_step": f"{round(lowest_value_temp_max_step, 2)} C",  # poprzednia temperatura
                         "value_of_max_step_one_hour": f"{current_max_value[1]} C",  # przed skokiem, wartość skoku
                         "initial_time_biggest_step": current_max_value[0],  # data z której pochodzi niższa wartość
                         "humidity_avg": humidity_avg,  # średnia wilgotność
                         "pressure_avg": pressure_avg},  # , średnia ciśnienie

            list_objects.insert(0, data_step)

            return Response(list_objects)
