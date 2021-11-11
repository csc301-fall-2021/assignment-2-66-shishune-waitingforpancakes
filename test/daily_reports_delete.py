import requests
url = "http://127.0.0.1:5000/daily_reports/"

r = requests.delete(url)
print(r)
