import requests
url = "http://127.0.0.1:5000/daily_reports/"

data = {"filetype":"csv", \
        "combined_key": 'Kerala, India', \
        "province_state": "",\
        "country_region":""}

print("we are gonna ask")
r = requests.get(url+"cases", data=data)
print("we got!", r, r.text)


