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

def format_by_type(text, t):
    if t >= 10 and t <= 12: # пракитка
        return "<i>" + text + "</i>" # italic
    if t >= 20 and t <= 24: # лабораторная
        return "<pre>" + text + "</pre>" # code
    if t >= 50 and t <= 55: # экзамен
        return "<b>" + text + "</b>" # bold
    return text     # default