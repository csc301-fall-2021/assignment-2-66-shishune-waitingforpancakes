# test cases
import unittest
import requests, os
from os.path import dirname

time_series_url = "http://127.0.0.1:5000/time_series/"
daily_reports_url = "http://127.0.0.1:5000/daily_reports/"

class TimeSeriesTests(unittest.TestCase):
    # def test_time_series_insert_confirmed(self):
    #     local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global_med.csv"
    #     data = open(local_file_to_send, "rb")
    #     response = requests.post(time_series_url+"confirmed", data=data)
    #     data.close()
    #     self.assertTrue(response.status_code == 200)

    # def test_time_series_insert_deaths(self):
    #     local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    #     data = open(local_file_to_send, "rb")
    #     response = requests.post(time_series_url+"deaths", data=data)
    #     data.close()
    #     self.assertTrue(response.status_code == 200)

    # def test_time_series_insert_recovered(self):
    #     local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    #     data = open(local_file_to_send, "rb")
    #     response = requests.post(time_series_url+"recovered", data=data)
    #     data.close()
    #     self.assertTrue(response.status_code == 200)

    def test_time_series_insert_noprovince(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_globalnoprov.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_insert_nocountry(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_globalnocountry.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_insert_wronglong(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global_bad.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_insert_outofrangedate(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/outofrangedate.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_insert_badformatdate(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/badformatdate.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_insert_nocountrycell(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/nocountry.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_insert_noprovincecell(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/noprovince.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_insert_noreportcell(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/noreportdata.csv"
        data = open(local_file_to_send, "rb")
        response = requests.post(time_series_url+"confirmed", data=data)
        data.close()
        self.assertTrue(response.status_code == 400)

    def test_time_series_query_deaths(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"deaths", data=data)
        content = {"filetype":"json", "deaths":True}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_confirmed(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "confirmed":True}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_recovered(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"recovered", data=data)
        content = {"filetype":"json", "recovered":True}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_one_day(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "start_date":"06/19/21", "end_date":"06/19/21"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_multiple_days(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "start_date":"06/19/21", "end_date":"06/21/21"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_combined_key(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "combined_key": "OntarioCanada"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_many_combined_key(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "combined_key": "OntarioCanada", "combined_key": "QuebecCanada"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_one_country_region(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "country_region": "Canada"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_many_country_region(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "country_region": "Canada", "country_region": "Russia"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_one_province(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "province_state": "Ontario"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_many_province(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "province_state": "Ontario", "province_state": "Quebec"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_json(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", \
            "query_type":"confirmed", \
            "province_state": "Bermuda", \
            "country_region":"Canada", \
            "country_region":"United Kingdom",\
            "start_date":"06/19/21", \
            "end_date":"06/19/21"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_csv(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"csv", \
            "query_type":"confirmed", \
            "province_state": "Bermuda", \
            "country_region":"Canada", \
            "country_region":"United Kingdom",\
            "start_date":"06/19/21", \
            "end_date":"06/19/21"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_missing_start_date(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", "start_date":"06/19/21"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_no_place_specified(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", \
            "query_type":"confirmed", \
            "start_date":"06/19/21", \
            "end_date":"06/19/21"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

    def test_time_series_query_no_time_specified(self):
        local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/csse_covid_19_time_series/querydata.csv"
        data = open(local_file_to_send, "rb")
        requests.post(time_series_url+"confirmed", data=data)
        content = {"filetype":"json", \
            "query_type":"confirmed", \
            "province_state": "Bermuda", \
            "country_region":"Canada", \
            "country_region":"United Kingdom"}
        response = requests.get(time_series_url+"cases", data=content)
        data.close()
        self.assertTrue(response.status_code == 200)

# class DailyReportTests(unittest.TestCase):
#      def test_daily_report_insert_noprovince(self):
#         local_file_to_send = os.path.dirname(dirname(dirname(os.getcwd()))) + "/Downloads/csse_covid_19_data/01-01-2021-bad-header.csv"
#         data = open(local_file_to_send, "rb")
#         response = requests.post(daily_reports_url, data=data)
#         data.close()
#         self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()

