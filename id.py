def subject_full_name(obj, id):
    try:
        for s in obj["subjects"]:
            if s['id'] == id:
                return s["title"]
        return "Not found"
    except:
        return "Not found"

def subject_short_name(obj, id):
    try:
        for s in obj["subjects"]:
            if s['id'] == id:
                return s["brief"]
        return "Not found"
    except:
        return "Not found"

def teacher_full_name(obj,id):
    try:
        for t in obj["teachers"]:
            if t['id'] == id:
                return t['full_name']
        return "Not found"
    except:
        return "Not found"

def teacher_short_name(obj,id):
    try:
        for t in obj["teachers"]:
            if t['id'] == id:
                return t['short_name']
        return "Not found"
    except:
        return "Not found"


# import datetime
# import time 

# t = datetime.datetime.now()

# print (t)

# now = t + datetime.timedelta(days=1)

# print(t)

# s = str(now.day)+"."+str(now.month)+"."+str(now.year)
# t_start = time.strptime(s, '%d.%m.%Y')
# print(datetime.datetime.fromtimestamp(time.mktime(t_start)))
# s = str(now.day)+"."+str(now.month)+"."+str(now.year)
# s = str(now.day)+"."+str(now.month)+"."+str(now.year)
# s = str(now.day)+"."+str(now.month)+"."+str(now.year)