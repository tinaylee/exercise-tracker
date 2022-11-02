import requests
import datetime as dt
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv


basic = HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD"))
load_dotenv("./.env")


def get_time():
    now = dt.datetime.now()
    current_time = now.time().replace(second=0, microsecond=0)
    return current_time


exercise_params = {
    "query": input("What exercise did you do? "),
    "gender": "female",
    "weight_kg": 43,
    "height_cm": 160,
    "age": 38
}

EXERCISE_HEADERS = {
    "x-app-id": os.getenv("APP_ID"),
    "x-app-key": os.getenv("API_KEY"),
    "x-remote-user-id": "0"
}

AUTH_HEADER = {
    "Authorization": "Basic d29ya291dF9zdHVmZjp3b3Jrb3V0MTIzNDU="
}

response = requests.post(url=os.getenv("EXERCISE_ENDPOINT"), json=exercise_params, headers=EXERCISE_HEADERS)
my_workout = response.json()

exercise_type = my_workout['exercises'][0]['user_input'].title()
exercise_duration = my_workout['exercises'][0]['duration_min']
exercise_calories = my_workout['exercises'][0]['nf_calories']

today = dt.date.today()

new_workout_data = {
    "workout": {
        "date": today.strftime("%d/%m/%Y"),
        "time": str(get_time()),
        "exercise": exercise_type,
        "duration": exercise_duration,
        "calories": exercise_calories
    }
}

response = requests.post(url=os.getenv("SHEETY_ENDPOINT"), json=new_workout_data, headers=AUTH_HEADER)
print(response.text)

