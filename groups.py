import urllib3
import json

url = "http://cist.nure.ua/ias/app/tt/P_API_GROUP_JSON"

http = urllib3.PoolManager()
r = http.request('GET', url)
cyrillic = r.data.decode('cp1251')

DATA = json.loads(r.data.decode('cp1251'))