
# Project description

This project aim to get forecast for previous 3 days before currently day. This project use django rest framework where I send api request on 
https://openweathermap.org/api/hourly-forecast. Then I use timemachine which allow me to get three days hourly forcast before currently day.

## 1. Hourly forecast for previous 3 days, django rest framework GUI

![Zrzut ekranu 2021-04-2 o 13 41 18](https://user-images.githubusercontent.com/56914063/113413139-3954f000-93ba-11eb-9120-de1e23020a65.png)

## 2. The time when temperature was started to rise, for previous 3 days forecast, and saving as a data.json file

![Zrzut ekranu 2021-04-22 o 14 31 36](https://user-images.githubusercontent.com/56914063/115714531-7ee05980-a377-11eb-9c72-3369adc96b3c.png)


## 3. Data of temperature growth. Django Rest Framework GUI.

![Zrzut ekranu 2021-04-16 o 18 20 26](https://user-images.githubusercontent.com/56914063/115054896-13af0700-9ee1-11eb-9050-deba70e67702.png)

## 4. List of lists with the biggest temperature step between the biggest and the lowest temperature value along with dates (isoformat ISO 8601).

![Zrzut ekranu 2021-04-17 o 18 25 07](https://user-images.githubusercontent.com/56914063/115120022-7cfb4c80-9fab-11eb-9934-98d8dd55c8fc.png)

## 5. The biggest temperature step between one hour of temperature growth.

### (Start date of growth, End date of growth, Value of step). Dates in ISO 8601.

![Zrzut ekranu 2021-04-18 o 22 08 39](https://user-images.githubusercontent.com/56914063/115159459-79db8b80-a093-11eb-9d2e-386f9bb6e94e.png)

## 6. Start time of growth, duration of growth, initial and end temp of growth.

<img width="779" alt="Zrzut ekranu 2021-04-27 o 13 43 35" src="https://user-images.githubusercontent.com/56914063/116236864-d9a2f800-a75f-11eb-9239-2d77cbd1de57.png">


## 7. Average value of humidity and pressure, initial time, the max value of step in increasing period of time within one hour, lowest value of temp when the max value of step exist, end time of max temp step. 

![Zrzut ekranu 2021-04-27 o 13 50 23](https://user-images.githubusercontent.com/56914063/116238067-39e66980-a761-11eb-928b-c74b56903c2a.png)











