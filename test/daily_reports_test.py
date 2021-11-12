# test cases
import unittest
import requests, os
from os.path import dirname

daily_reports_url = "http://127.0.0.1:5000/daily_reports/"

class DailyReportTests(unittest.TestCase):
    def test_daily_report_insert_bad_header(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/bad-header.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_daily_report_insert_missing_header(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/missing-header.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_daily_report_insert_no_key(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/no-key.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_daily_report_insert_null_confirmed(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/nul-val-confirmed.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)
    
    def test_daily_report_insert_null_deaths(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/nul-val-deaths.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_daily_report_insert_null_recovered(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/nul-val-recovered.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_daily_report_insert_null_active(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/nul-val-active.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_daily_report_insert_poorly_formatted_date(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/poorly-formatted-date.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_daily_report_insert_illegal_date(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/illegal-date.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_daily_report_insert_proper_file(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_daily_report_insert_update_file(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        get_data = {"filetype":"csv", \
        "combined_key": 'Afghanistan', \
        "province_state": "",\
        "country_region":"", \
        "confirmed": True, 
        "deaths": True, 
        "recovered": True, 
        "active": True}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(r.text.split()[1]=="0,,Afghanistan,Afghanistan,2021/01/03,52513,2201,41727,0")
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/update.csv"
        
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(r.text.split()[1]=="0,,Afghanistan,Afghanistan,2021/01/03,0,0,10000,0")

    def test_daily_report_get_all_data(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", \
        "confirmed": True, 
        "deaths": True, 
        "recovered": True, 
        "active": True}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        text = r.text.split('\n')
        self.assertTrue(len(text) == 17)
        self.assertTrue(len(text[0].split(',')) == 9)

    def test_daily_report_get_confirmed(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", \
        "confirmed": True}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        text = r.text.split('\n')
        self.assertTrue(len(text) == 17)
        self.assertTrue(len(text[0].split(',')) == 6)

    def test_daily_report_get_deaths(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", \
        "deaths": True}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        text = r.text.split('\n')
        self.assertTrue(len(text) == 17)
        self.assertTrue(len(text[0].split(',')) == 6)

    def test_daily_report_get_recovered(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", \
        "recovered": True}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        text = r.text.split('\n')
        self.assertTrue(len(text) == 17)
        self.assertTrue(len(text[0].split(',')) == 6)

    def test_daily_report_get_active(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", \
        "active": True}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        text = r.text.split('\n')
        self.assertTrue(len(text) == 17)
        self.assertTrue(len(text[0].split(',')) == 6)

    def test_daily_report_get_no_count(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":""}
        
        r = requests.get(daily_reports_url+"cases", data=get_data)
        text = r.text.split('\n')
        self.assertTrue(len(text) == 17)
        self.assertTrue(len(text[0].split(',')) == 5)
        

    def test_daily_report_get_one_date(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", 
        "date": "2021-01-03"}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 3)

    def test_daily_report_get_one_date(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", 
        "date": "2021-01-01,2021-01-02,2021-01-03"}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 15)


    def test_daily_report_get_many_date(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "", \
        "province_state": "",\
        "country_region":"", 
        "date": "2021-01-01,2021-01-02,2021-01-03"}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 15)

    def test_daily_report_get_one_key(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "Australian Capital Territory, Australia", \
        "province_state": "",\
        "country_region":"", 
        "date": ""}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 3)

    def test_daily_report_get_many_keys(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "combined_key": "'Australian Capital Territory, Australia','New South Wales, Australia'", \
        "province_state": "",\
        "country_region":"", 
        "date": ""}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 4)

    def test_daily_report_get_one_country(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "province_state": "",\
        "country_region":"Australia", 
        "date": ""}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 9)
   
    def test_daily_report_get_many_country(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "province_state": "",\
        "country_region":"Australia,Afghanistan", 
        "date": ""}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 10)

    def test_daily_report_get_one_province(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "province_state": "New South Wales",\
        "country_region":"", 
        "date": ""}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 3)

    def test_daily_report_get_many_province(self):
        response = requests.delete(daily_reports_url)

        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv", \
        "province_state": "New South Wales,Queensland",\
        "country_region":"", 
        "date": ""}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(len(r.text.split('\n')) == 4)

    def test_daily_report_get_csv(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"csv"}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(r.status_code == 200)

    def test_daily_report_get_json(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {"filetype":"json"}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(r.status_code == 200)

    def test_daily_report_get_no_file_type(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/dailyquery.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(daily_reports_url, data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

        get_data = {}

        r = requests.get(daily_reports_url+"cases", data=get_data)
        self.assertTrue(r.status_code == 400)

        
if __name__ == '__main__':
    unittest.main()
