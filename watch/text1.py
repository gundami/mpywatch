import requests
import json
LURL = 'http://ipinfo.io/json'
result = requests.get(LURL).text
j = json.loads(result)
loca = j['region']
URL = 'https://api.seniverse.com/v3/weather/now.json?key=Sc7N7OW6wil2inCFV&location='+loca+'&language=en&unit=c'
result = requests.get(URL).text
j = json.loads(result)
location=j['results'][0]['location']['name']
text=j['results'][0]['now']['text']
temp=j['results'][0]['now']['temperature']
print(location)
print(temp)
print(text)