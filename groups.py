import urllib3
import json

url = "http://cist.nure.ua/ias/app/tt/P_API_GROUP_JSON"

http = urllib3.PoolManager()
r = http.request('GET', url)
cyrillic = r.data.decode('cp1251')

a = type(r)

DATA = json.loads(r.data.decode('cp1251'))


string = "line for debug"

# def group_name(group_id):
#     url = "http://cist.nure.ua/ias/app/tt/P_API_EVENTS_GROUP_JSON?p_id_group="
#     url += str(group_id)
#     r = http.request('GET', url)
#     data = json.loads(r.data.decode('cp1251'))
#     for g in data['groups']:
#         if g['id'] == group_id:
#             return g['name']
