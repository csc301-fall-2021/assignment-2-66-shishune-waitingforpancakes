import requests, os
from os.path import dirname

url = "http://127.0.0.1:5000/time_series/"

# my file to be sent
local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
data = open(local_file_to_send, "r")

print("we are gonna send")
r = requests.post(url+"confirmed", data=data)
print("we sent!")
print(r.status_code, r.text)



