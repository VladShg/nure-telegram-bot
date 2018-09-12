import urllib3
import json

url = "http://cist.nure.ua/ias/app/tt/P_API_GROUP_JSON"

http = urllib3.PoolManager()
r = http.request('GET', url)
cyrillic = r.data.decode('cp1251')

DATA = json.loads(r.data.decode('cp1251'))


# string = "line for debug"

# url2 = "http://cist.nure.ua/ias/app/tt/P_API_EVEN_JSON?timetable_id=6496579&type_id=1&time_from=1535760000&time_to=1543622400"
# r2 = http.request('GET', url2)

# cyrillic2 = r2.data.decode('cp1251')

# DATA2 = json.loads(r2.data.decode('cp1251'))

# string = "line for debug"

# def group_name(group_id):
#     url = "http://cist.nure.ua/ias/app/tt/P_API_EVENTS_GROUP_JSON?p_id_group="
#     url += str(group_id)
#     r = http.request('GET', url)
#     data = json.loads(r.data.decode('cp1251'))
#     for g in data['groups']:
#         if g['id'] == group_id:
#             return g['name']
