import requests, os
from os.path import dirname
import pandas as pd

url = "http://127.0.0.1:5000/time_series/"

data = {"filetype":"csv", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}

print("we are gonna ask")
r = requests.get(url+"cases", data=data)
print("we got!")