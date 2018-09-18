import psycopg2
from psycopg2.extras import Json
import os
import urllib3
import json

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()
TEACHERS = dict()
GROUPS = dict()

def subject_full_name(obj, id):
    try:
        for s in obj:
            if s['id'] == id:
                return s["title"]
        return "Not found"
    except:
        return "Not found"

def subject_short_name(obj, id):
    try:
        for s in obj:
            if s['id'] == id:
                return s["brief"]
        return "Not found"
    except:
        return "Not found"

def teacher_full_name(obj,id):
    try:
        for t in obj:
            if t['id'] == id:
                return t['full_name']
        return "Not found"
    except:
        return "Not found"

def teacher_short_name(obj,id):
    try:
        for t in obj:
            if t['id'] == id:
                return t['short_name']
        return "Not found"
    except:
        return "Not found"

def format_by_type(text, t):
    if t >= 10 and t <= 12: # пракитка
        return "<a href=\"https://ne-nuzhno-syuda-nazhima.tb\">" + text + "</a>" # Ссылка
    if t >= 20 and t <= 24: # лабораторная
        return "<code>" + text + "</code>" # code
    if t >= 50 and t <= 55: # экзамен
        return "<b>" + text + "</b>" # bold
    return text     # default

    # Не использовал italic, потому что при малом обьеме текста очень слабо заметно различия с лекцией

def weekday(num):
    if num == 0:
        return "Понедельник"
    if num == 1:
        return "Вторник"
    if num == 2:
        return "Среда"
    if num == 3:
        return "Четверг"
    if num == 4:
        return "Пятница"
    if num == 5:
        return "Суббота"
    if num == 6:
        return "Воскресенье"