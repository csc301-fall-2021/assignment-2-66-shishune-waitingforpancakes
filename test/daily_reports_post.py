import requests, os
from os.path import dirname
import pandas as pd

url = "http://127.0.0.1:5000/daily_reports/"

# my file to be sent
local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_daily_reports/01-02-2021.csv"
data = open(local_file_to_send, "r")
print("we are gonna send")
r = requests.post(url, data=data)
print("we are sending")
print(r, r.status_code, r.text)
#print(str(r.content, 'utf-8'))