import requests
import json
URL = 'http://ipinfo.io/json'
result = requests.get(URL).text
j = json.loads(result)
location=j['region']
print(location)
