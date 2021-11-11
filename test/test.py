# test cases
import unittest
import app.py
import requests, os
from os.path import dirname

time_series_url = "http://127.0.0.1:5000/time_series/"
daily_reports_url = "http://127.0.0.1:5000/daily_reports/"

def time_series_insert_confirmed():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global_bad.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 200

def time_series_insert_deaths():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global_bad.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"deaths", data=data)
    assert response.status_code == 200

def time_series_insert_recovered():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global_bad.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"recovered", data=data)
    assert response.status_code == 200

def time_series_insert_noprovince():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_globalnoprov.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 200

def time_series_insert_nocountry():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_globalnocountry.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 400

def time_series_insert_wronglong():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global_bad.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 400

def time_series_insert_outofrangedate():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/outofrangedate.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 400

def time_series_insert_badformatdate():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/badformatdate.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 400

def time_series_insert_nocountrycell():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/nocountry.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 400

def time_series_insert_noprovincecell():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/noprovince.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 200

def time_series_insert_noreportcell():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/noreportdata.csv"
    data = open(local_file_to_send, "r")
    response = requests.post(time_series_url+"confirmed", data=data)
    assert response.status_code == 400

def time_series_query_deaths():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"deaths", data=data)
    content = data = {"filetype":"json", "deaths":True}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 200

def time_series_query_confirmed():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", "confirmed":True}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 200

def time_series_query_recovered():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"recovered", data=data)
    content = data = {"filetype":"json", "recovered":True}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 200

def time_series_query_one_day():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", "start_date":"06/19/21", "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query_multiple_days():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
        content = data = {"filetype":"json", "start_date":"06/19/21", "end_date":"06/21/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query_combined_key():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", "combined_key": "OntarioCanada"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400

def time_series_query():
    local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
    data = open(local_file_to_send, "r")
    requests.post(time_series_url+"confirmed", data=data)
    content = data = {"filetype":"json", \
        "query_type":"confirmed", \
        "province_state": "Bermuda", \
        "country_region":"Canada", \
        "country_region":"United Kingdom",\
        "start_date":"06/19/21", \
        "end_date":"06/19/21"}
    r = requests.get(url+"cases", data=content)
    assert response.status_code == 400



