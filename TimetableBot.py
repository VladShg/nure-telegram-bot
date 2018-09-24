from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import db
from psycopg2.extras import Json
from multiprocessing import Process
import psycopg2
import os
import datetime
import schedule
import time
import ast
import urllib3
import json
import os
import random
from time import sleep
from timeObj import timeObj
import id
from id import subject_full_name, subject_short_name, weekday, \
               teacher_full_name, teacher_short_name, format_by_type
from config import TOKEN, MY_ID, StatesGroup
from groups import DATA
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

def connection():
    global conn
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    global c
    c = conn.cursor()

def update_data():
    connection()
    print("inside update")
    with conn:
        c.execute("SELECT * FROM cache")
        start = datetime.datetime.now()
        groups = c.fetchall()
        l = len(groups)
        for g in groups:
            url = g[6]
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            obj = json.loads(r.data.decode('cp1251'))
            c.execute("UPDATE cache SET events = {}, teachers = {}, subjects = {}, types = {} WHERE id={}".format(Json(obj['events']),
                     Json(obj['teachers']), Json(obj['subjects']), Json(obj['types']), g[0]))
        end = datetime.datetime.now()
    print("Обновлено {} елементов {}-{}".format(l, start.strftime("%H:%M:%S"), end.strftime("%H:%M:%S")))

def register(msg):
    connection()
    with conn:
        c.execute("SELECT * FROM users WHERE id={}".format(msg.from_user.id))
        if len(list(c.fetchall())) == 0:
            c.execute("INSERT INTO users(id, name, short_subj, short_teacher, faculty_name, group_name, group_id, last_update, updates, grp_state, notify, time_state, pair_state) VALUES ({}, {}, 1, 1, '', '', -1, CURRENT_TIMESTAMP , 1, {}, 1, 0, 0);".format(msg.from_user.id, \
             "'" +msg.from_user.full_name + "'", StatesGroup.S_NONE.value))
        else:
            c.execute("SELECT * FROM users WHERE id={}".format(msg.from_user.id))
            obj = c.fetchone()
            num = obj[8] + 1
            c.execute("UPDATE users SET last_update= CURRENT_TIMESTAMP, updates={}, name='{}' WHERE id={}".format(num, msg.from_user.full_name, msg.from_user.id))
            
def update(msg):
    connection()
    c.execute("SELECT * FROM users WHERE id={}".format(msg.from_user.id))
    obj = c.fetchone()
    num = obj[8] + 1
    c.execute("UPDATE users SET last_update= CURRENT_TIMESTAMP, updates={}, name='{}' WHERE id={}".format(num, msg.from_user.full_name, msg.from_user.id))

def set_state(id, num):
    connection()
    with conn:
        c.execute("UPDATE users SET grp_state ={} WHERE id = {}".format(num, id))

def get_state(id):
    connection()
    with conn:
        c.execute("SELECT * FROM users WHERE id = {}".format(id))
        obj = c.fetchone()
        return obj[9]

def boolChange(id, key):
    connection()
    with conn:
        c.execute("SELECT * FROM users WHERE id={}".format(id))
        user = c.fetchone()
        val = 0
        if key == "short_teacher":
            n = 3
            val = 1
            if user[n] == 1:
                val = 0
        elif key == "short_subj":
            n = 2
            val = 1
            if user[n] == 1:
                val = 0
        elif key == "time_state":
            n = 11
            if user[n] == 0:
                val = 1
            if user[n] == 1:
                val = 0
        elif key == "pair_state":
            n = 12
            if user[n] == 0:
                val = 1
            if user[n] == 1:
                val = 0
        elif key == "notify":
            n = 10
            val = 1
            if user[n] == 1:
                val = 0
        
        c.execute("UPDATE users SET " + key + " ={} WHERE id={}""".format(val,id))

async def timetable(id, num):
    connection()
    short_t = 0
    short_s = 0
    group_id = 0
    with conn:
        c.execute("SELECT * FROM users WHERE id = {}".format(id))
        user = c.fetchone()
        short_t = user[3]
        short_s = user[2]
        group = user[5]
        group_id = user[6]
        pair_time = user[11]
        pair_state = user[12]
        if user[6] == -1:
            await bot.send_message(id, "Не указана группа", reply_markup=kb_start)
            return

    s_start = datetime.datetime.now()
    s_start -= datetime.timedelta(days=1)
    if s_start.hour >= 19:
        s_start += datetime.timedelta(days=1)

    with conn:
        c.execute("SELECT * FROM cache WHERE name='{}'".format(group))
        result = c.fetchall()
        if len(result) == 0:
            url = "http://cist.nure.ua/ias/app/tt/P_API_EVEN_JSON?timetable_id=" + str(group_id)
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            obj = json.loads(r.data.decode('cp1251'))
            c.execute("INSERT INTO cache(id, name, events, teachers, subjects, types, url) VALUES({}, '{}', {}, {}, {}, {}, '{}')".format(group_id,
                    group, Json(obj['events']), Json(obj['teachers']), Json(obj['subjects']),
                    Json(obj['types']), url))
            events = obj['events']
            teachers = obj['teachers']
            subjects = obj['subjects']
        else:
            events = result[0][2]
            teachers = result[0][3]
            subjects = result[0][4]

    dates = list()
    for i in range(num):
        dates.append((datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d.%m.%Y"))

    event_day = dict()

    for e in events:
        key = e["start_time"]
        t = datetime.datetime.fromtimestamp(key)
        key = t.strftime("%d.%m.%Y")
        if key in dates:
            try:
                event_day[key].append(e)
            except:
                event_day[key] = list()
                event_day[key].append(e)

    # for i in range(num):
    #     key = key = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d.%m.%Y")
    #     try:
    #         for event in events[key]:
    #             try:
    #                 total[key].append(event)
    #             except:
    #                 total[key] = list()
    #                 total[key].append(event)
    #     except:
    #         continue
        
    if len(event_day) == 0:
        await bot.send_message(id, "Пар не найдено", reply_markup=kb_start)

    start = ['7:45', "9:30", "11:15", "13:10", "14:55", "16:40"]
    end = ['9:20', "11:05", "12:50", "14:45", "16:30", "18:15"]


    for k in event_day:
        d = datetime.datetime.fromtimestamp(event_day[k][0]['start_time'])
        s = k
        s += " " + weekday(d.weekday())  + "\n"

        for e in event_day[k]:
            s += '\n'
            # s += "[" + str(start[e['number_pair'] - 1]) + "-" + str(end[e['number_pair'] - 1]) + "] " + "[" + e['auditory'] + "] "
            
            if pair_state == 1:
                s += str(e['number_pair']) + ") "
            if pair_time == 1:
                s += str(start[e['number_pair'] - 1]) + "-" + str(end[e['number_pair'] - 1]) + " "
            a = subject_full_name(subjects, e["subject_id"])
            if short_s == 1:
                a = subject_short_name(subjects, e["subject_id"])
            s += format_by_type(a, e['type'])
            s += " " + e['auditory'] + " "
            if len(e['teachers']) > 0:
                s += "\n"
                a = teacher_full_name(teachers, e['teachers'][0])
                if short_t == 1:
                    a = teacher_short_name(teachers, e['teachers'][0])
                s += a
                
        await bot.send_message(id, s, reply_markup=kb_start, parse_mode="HTML")
        if num >= 7:
            time.sleep(0.3)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

@dp.message_handler(commands=['gr'])
async def process_group_command(msg: types.Message):
    faculties = DATA['university']['faculties']
    kb_fac = InlineKeyboardMarkup(row_width=3)
    set_state(msg.from_user.id, StatesGroup.S_ENTER_FAC.value)
    for n in range(len(faculties)):
        data = dict()
        data['f'] = n
        kb_fac.insert(InlineKeyboardButton(faculties[n]['full_name'], callback_data=str(data)))
    await bot.send_message(msg.from_user.id, text="Факультет: ", reply_markup=kb_fac)

@dp.callback_query_handler(func=lambda message: get_state(message.message.chat.id) == StatesGroup.S_ENTER_FAC.value)
async def process_callback_enter_fac(call: types.CallbackQuery):
    set_state(call.message.chat.id, StatesGroup.S_ENTER_DIR.value)
    data = eval(call.data)
    faculty = DATA['university']['faculties'][data['f']]
    kb_dir = InlineKeyboardMarkup(row_width=3)
    for d in range(len(faculty['directions'])):
        data['d'] = d
        kb_dir.insert(InlineKeyboardButton(faculty['directions'][d]['full_name'], callback_data = str(data)))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Факультет: {}\n\nСпециальность:".format(faculty['full_name']), reply_markup = kb_dir)

@dp.callback_query_handler(func=lambda message: get_state(message.message.chat.id) == StatesGroup.S_ENTER_DIR.value)
async def process_callback_enter_dir(call: types.CallbackQuery):
    set_state(call.message.chat.id, StatesGroup.S_ENTER_GROUP.value)
    #Веломарафон, специальная олимпиада 07.09.2018-08.09.2018
    #Почестный участник: Vled
    
    # try:
    #     for f in DATA['university']['faculties']:
    #         for d in f['directions']:
    #             if d['full_name'] == call.data:
    #                 direction = d
    #                 faculty = f
    #                 raise Exception("Out from search loop")
    # except:
    #     s = "gtfo"

    # Веломарафон отменили

    data = eval(call.data)

    faculty = DATA['university']['faculties'][data['f']]
    direction = faculty['directions'][data['d']]

    kb_group = InlineKeyboardMarkup(row_width=3)

    for g in range(len(direction['groups'])):
        data['g'] = g
        kb_group.insert(InlineKeyboardButton(text=direction['groups'][g]['name'], callback_data=str(data)))

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Факультет: {}\nСпециальность: {}".format(faculty['full_name'], direction['full_name']), reply_markup = kb_group)    

@dp.callback_query_handler(func=lambda message: get_state(message.message.chat.id) == StatesGroup.S_ENTER_GROUP.value)
async def process_callback_enter_group(call: types.CallbackQuery):
    connection()
    data = eval(call.data)
    faculty = DATA['university']['faculties'][data['f']]
    direction = faculty['directions'][data['d']]
    group = direction['groups'][data['g']]
    with conn:
        c.execute("UPDATE users SET group_id = {}, group_name='{}', faculty_name ='{}' WHERE id={}".format(group['id'], \
        group['name'], faculty['full_name'], call.message.chat.id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, \
     text="Факультет: {}\nСпециальность: {}\nГруппа: {}".format(faculty['full_name'], direction['full_name'], group['name']))
    await bot.send_message(call.message.chat.id, "Изменения вступили в силу", reply_markup=kb_start)        

@dp.callback_query_handler(func=lambda message: get_state(message.message.chat.id) == StatesGroup.S_NONE.value)
async def process_callback_timetable_swift(call: types.CallbackQuery):
        connection()

        set_state(call.message.chat.id, StatesGroup.S_NONE.value)

        shift = int(call.data)

        kb_navigate = InlineKeyboardMarkup(row_width=3)
        kb_navigate.insert(InlineKeyboardButton(text="⏪", callback_data=str(shift - 1)))
        kb_navigate.insert(InlineKeyboardButton(text="🔄", callback_data=str(shift)))
        kb_navigate.insert(InlineKeyboardButton(text="⏩", callback_data=str(shift + 1)))

        with conn:
            c.execute("SELECT * FROM users WHERE id = {}".format(call.message.chat.id))
            user = c.fetchone()
            short_t = user[3]
            short_s = user[2]
            group = user[5]
            pair_time = user[11]
            pair_state = user[12]

        s_start = datetime.datetime.now()
        s_start += datetime.timedelta(days=shift)

        todayKey = s_start.strftime("%d.%m.%Y")

        with conn:
            c.execute("SELECT * FROM cache WHERE name='{}'".format(group))
            result = c.fetchall()
            events = result[0][2]
            teachers = result[0][3]
            subjects = result[0][4]

        event_day = list()
        for e in events:
            key = e["start_time"]
            t = datetime.datetime.fromtimestamp(key)
            key = t.strftime("%d.%m.%Y")
            if key == todayKey:
                event_day.append(e)


        if len(event_day) == 0:
            s = s_start.strftime("%d.%m.%Y") + " " + weekday(s_start.weekday())
            try:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=s+ "\n\nПар не найдено", reply_markup=kb_navigate)
                await bot.answer_callback_query(callback_query_id=call.id)
            except:
                await bot.answer_callback_query(callback_query_id=call.id, text="Изменений нет")
            return

        timer = ""
        now = s_start + datetime.timedelta(hours=3)
        TIME = timeObj()
        if now.day >= datetime.datetime.strptime(todayKey, "%d.%m.%Y").day:
            n = event_day[len(event_day) - 1]['number_pair']
            timer += "\n\n"
            if shift > 0:
                    start = TIME['start'][event_day[0]['number_pair'] -1]
                    h = (24 - s_start.hour - 4) + start.hour
                    m = (60 - s_start.minute) + start.minute
                    s = (60 - s_start.second)
                    dlt = datetime.timedelta(days=shift - 1, hours=h, minutes=m, seconds=s)
                    timer += "До начала пар: " + str(dlt)

            else:
                if shift < 0:
                    timer = ""
                else:
                    if now > TIME['end'][n-1]:
                        timer += "Пары закончились, можно чилить"
                    else:
                        for e in event_day:
                            if now > TIME['start'][e['number_pair']-1] and now < TIME['end'][e['number_pair']-1]:
                                time = TIME['end'][e['number_pair']-1] - now()
                                timer += "До конца пары: " + time.strftime("%H:%M:%S")
                                break
                            if now < TIME['start'][e['number_pair']-1]:
                                time = TIME['start'][e['number_pair']-1] - now()
                                timer += "До начала пары: "
        
        start = ['7:45', "9:30", "11:15", "13:10", "14:55", "16:40"]
        end = ['9:20', "11:05", "12:50", "14:45", "16:30", "18:15"]

        s = todayKey + " " + weekday(s_start.weekday())  + "\n"
        for e in event_day:
            s += '\n'
            if pair_state == 1:
                s += str(e['number_pair']) + ") "
            if pair_time == 1:
                s += str(start[e['number_pair'] - 1]) + "-" + str(end[e['number_pair'] - 1]) + " "
            a = subject_full_name(subjects, e["subject_id"])
            if short_s == 1:
                a = subject_short_name(subjects, e["subject_id"])
            s += format_by_type(a, e['type'])
            s += " " + e['auditory'] + " "
            if len(e['teachers']) > 0:
                s += "\n"
                a = teacher_full_name(teachers, e['teachers'][0])
                if short_t == 1:
                    a = teacher_short_name(teachers, e['teachers'][0])
                s += a

        s += timer

        try:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=s, parse_mode="HTML", reply_markup=kb_navigate)
            await bot.answer_callback_query(callback_query_id=call.id)
        except:
            await bot.answer_callback_query(callback_query_id=call.id, text="Изменений нет")

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    register(message)
    set_state(message.from_user.id, StatesGroup.S_NONE.value)
    await bot.send_message(message.from_user.id, "Расписание\n\n🔀 — На день\n1️⃣ — На 1 день\n7️⃣ — На 7 дней\n🔢 — На 30 дней\n\n 🏠 — Стартовая страница /start\n ⚙️ — Настройки /settings", reply_markup=kb_start)

@dp.message_handler(commands=['db'])
async def process_db_command(message: types.Message):
    if message.from_user.id != MY_ID:
        await bot.send_message(message.from_user.id, "sosi hui")
        return
    connection()    
    with conn:
        c.execute("SELECT * FROM users")
        lst = c.fetchall()
        s = ""
        for n in range(len(lst)):
            if len(s) != 0:
                s += "\n"
            s += str(lst[n])
            if n % 5 == 0 :
                await bot.send_message(message.from_user.id, s)
                s = ""
        if len(s) != 0:
            await bot.send_message(message.from_user.id, s)
            
@dp.message_handler(commands=['dbf'])
async def process_dbf_command(message: types.Message):
    if message.from_user.id != MY_ID:
        await bot.send_message(message.from_user.id, "sosi hui")
        return
    with conn:
        c.execute("SELECT * FROM users")
        lst = sorted(c.fetchall(), key=lambda tup: tup[7])
        s = ""
        for n in range(len(lst)):
            s += lst[n][1] + " "
            H = lst[n][7].hour + 3
            s += lst[n][7].strftime("%d.%m {}:%M").format(str(H)) + " "
            s += str(lst[n][8]) + " "
            s += str(lst[n][10])
            if n % 10 == 0 and n != 0:
                await bot.send_message(message.from_user.id, s)
                s = ""
            else:
                s += "\n"
        if n % 10 != 0:
            await bot.send_message(message.from_user.id, s)
        
@dp.message_handler(commands=['update'])
async def process_update_command(message: types.Message):
    update_data()

@dp.message_handler(commands=["tn"])
async def teacher_name_change(msg: types.Message):
    boolChange(msg.from_user.id, "short_teacher")
    await process_settings_command(msg)

@dp.message_handler(commands=["sn"])
async def subject_name_change(msg: types.Message):
    boolChange(msg.from_user.id, "short_subj")
    await process_settings_command(msg)

@dp.message_handler(commands=["pn"])
async def pair_number_change(msg: types.Message):
    boolChange(msg.from_user.id, "pair_state")
    await process_settings_command(msg)

@dp.message_handler(commands=["pt"])
async def pair_time_change(msg: types.Message):
    boolChange(msg.from_user.id, "time_state")
    await process_settings_command(msg)

@dp.message_handler(commands=["nt"])
async def notify_change(msg: types.Message):
    boolChange(msg.from_user.id, "notify")
    await process_settings_command(msg)

# region do not enter

# @dp.message_handler(commands=["random"])
# async def process_random_handler(message: types.Message):
#     files = list()
#     for f in os.listdir("random/"):
#         files.append(f.split(".")[0])
#     i = random.randrange(len(files))
#     f = open('random/'+files[i]+".png", 'rb')
#     await bot.send_photo(message.from_user.id, caption = files[i], reply_markup=kb_additional,
#                     photo=f)

# @dp.message_handler(commands=["lazyrandom"])
# async def process_lazyrandom_handler(message: types.Message):
#     files = list()
#     for f in os.listdir("random/"):
#         files.append(f.split(".")[0])
#     for f in files:
#         fl = open('random/'+ f +".png", 'rb')
#         await bot.send_photo(message.from_user.id, caption = f, reply_markup=kb_additional,
#                     photo=fl)

# endregion

@dp.message_handler(regexp="\A(⚙️)\Z")
async def process_emoji_settings_command(msg: types.Message):
    await process_settings_command(msg)

@dp.message_handler(commands=['settings'])
async def process_settings_command(msg: types.Message):
    register(msg)
    set_state(msg.from_user.id, StatesGroup.S_NONE.value)
    connection()
    with conn:
            c.execute("SELECT * FROM users WHERE id={}".format(msg.from_user.id))
            user = c.fetchone()

            group = "Не указано"
            if user[6] != -1:
                group = user[5]

            full_s = "✅"
            if user[2] == 1:
                full_s = "❌"

            full_t = "✅"
            if user[3] == 1:
                full_t = "❌"

            notify = "❌"
            if user[10] == 1:
                notify = "✅"

            pair_num = "❌"
            if user[12] == 1:
                pair_num = "✅"

            pair_time = "❌"
            if user[11] == 1:
                pair_time = "✅"

            string = "Настройки\n\n"
            string += "Группа: {} /gr\n".format(group)
            string += "Полные имена предметов: {} /sn\n".format(full_s)
            string += "Полные имена преподавателей: {} /tn\n".format(full_t)
            string += "Номер пары: {} /pn\n".format(pair_num)
            string += "Время пары: {} /pt\n".format(pair_time)
            string += "Сообщения: {} /nt\n".format(notify)
            string += "\n "
            string += "🔍 Справка /help"
            # string += "\n"
            # string += "💙 /random "

            await bot.send_message(msg.from_user.id, string, reply_markup=kb_settings)

@dp.message_handler(commands=['help'])
async def process_info_command(msg: types.Message):
    set_state(msg.from_user.id, StatesGroup.S_NONE.value)
    # s = "/random - разное из процесса разработки, пока что только 4 записи"
    # s += "\n"
    # s += "/lazyrandom - для ленивых"
    # s += "\n\n"
    s = "Разметка: \n"
    s += format_by_type("Лекция", 0) + "\n"
    s += format_by_type("Практика", 11) + "\n"
    s += format_by_type("Лабораторная", 22) + "\n"
    s += format_by_type("Экзамен", 50) + "\n"
    # s += "\n\n"
    # s += "Планы на будущее: напоминания, таймер до конца пары, расписание для преподавателя, фильтр предметов.\n"
    # s += "Автор не претендует на оригинальность или конкуренцию с более ранними приложениями"
    s += "\n\n"
    s += "Обратная связь: @VledSh"
    await bot.send_message(msg.from_user.id, s, reply_markup=kb_additional, parse_mode="HTML")

@dp.message_handler(regexp="\A(🔍)\Z")
async def process_info_emoji_command(msg: types.Message):
    await process_info_command(msg)

@dp.message_handler(regexp="\A(/alarm)")
async def alarm_command(msg: types.Message):
    s = msg.text[7:]
    s += "\n\nОтключить сообщения: /nt"
    if msg.from_user.id != MY_ID:
        await bot.send_message(msg.from_user.id, "Нужны права администратора", reply_markup=kb_additional)
        return
    if len(msg.text) <= 7:
        await bot.send_message(msg.from_user.id, "Пустое сообщение", reply_markup=kb_start)
        return
    with conn:
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        for u in users:
            if u[10] == 1:
                try:
                    f = open('notification/update.png', 'rb')
                    await bot.send_photo(u[0], caption = s, reply_markup=kb_additional, photo=f)
                    time.sleep(1)
                except Exception as e: 
                    await bot.send_message(MY_ID, str(e) + " " + u[1])
                    time.sleep(1)

@dp.message_handler(regexp="\A(/sendm)")
async def process_sendm_command(message: types.Message):
    id = int(message.text[7:16])
    msg = message.text[17:]
    try:
        await bot.send_message(str(id), msg)
    except Exception as e:
        await bot.send_message(MY_ID, str(e))

@dp.message_handler(regexp="\A(🔀)\Z")
async def process_timetable_custom_command(msg: types.Message):
        connection()        
        register(msg)
        
        set_state(msg.from_user.id, StatesGroup.S_NONE.value)
        shift = 0
        kb_navigate = InlineKeyboardMarkup(row_width=3)
        kb_navigate.insert(InlineKeyboardButton(text="⏪", callback_data=str(shift - 1)))
        kb_navigate.insert(InlineKeyboardButton(text="🔄", callback_data=str(shift)))
        kb_navigate.insert(InlineKeyboardButton(text="⏩", callback_data=str(shift + 1)))
        short_t = 0
        short_s = 0
        group_id = 0

        todayKey = datetime.datetime.now().strftime("%d.%m.%Y")

        with conn:
            c.execute("SELECT * FROM users WHERE id = {}".format(msg.from_user.id))
            user = c.fetchone()
            short_t = user[3]
            short_s = user[2]
            group = user[5]
            group_id = user[6]
            pair_time = user[11]
            pair_state = user[12]
            if user[6] == -1:
                await bot.send_message(msg.from_user.id, "Не указана группа", reply_markup=kb_start)
                return

        with conn:
            c.execute("SELECT * FROM cache WHERE name='{}'".format(group))
            result = c.fetchall()
            if len(result) == 0:
                url = "http://cist.nure.ua/ias/app/tt/P_API_EVEN_JSON?timetable_id=" + str(group_id)
                http = urllib3.PoolManager()
                r = http.request('GET', url)
                obj = json.loads(r.data.decode('cp1251'))
                c.execute("INSERT INTO cache(id, name, events, teachers, subjects, types, url) VALUES({}, '{}', {}, {}, {}, {}, '{}')".format(group_id,
                        group, Json(obj['events']), Json(obj['teachers']), Json(obj['subjects']),
                        Json(obj['types']), url))
                events = obj['events']
                teachers = obj['teachers']
                subjects = obj['subjects']
                typs = obj['types']
            else:
                events = result[0][2]
                teachers = result[0][3]
                subjects = result[0][4]
                typs = result[0][5]        

        event_day = list()

        for e in events:
            key = e["start_time"]
            t = datetime.datetime.fromtimestamp(key)
            key = t.strftime("%d.%m.%Y")
            if key == todayKey:
                event_day.append(e)

        start = ['7:45', "9:30", "11:15", "13:10", "14:55", "16:40"]
        end = ['9:20', "11:05", "12:50", "14:45", "16:30", "18:15"]

        if len(event_day) == 0:
            d = datetime.datetime.now()
            s = d.strftime("%d.%m.%Y") + " " + weekday(d.weekday())
            await bot.send_message(msg.from_user.id, s+ "\n\nПар не найдено", reply_markup=kb_navigate)
            return

        timer = ""
        TIME = timeObj()
        now = datetime.datetime.now() + datetime.timedelta(hours=3)
        if now.day >= datetime.datetime.strptime(todayKey, "%d.%m.%Y").day:
            n = event_day[len(event_day) - 1]['number_pair']
            timer += "\n\n"
            if now > TIME['end'][n-1]:
                timer += "Пары закончились, можно чилить"
            else:
                for e in event_day:
                    if now > TIME['start'][e['number_pair']-1] and now < TIME['end'][e['number_pair']-1]:
                        time = TIME['end'][e['number_pair']-1] - now
                        timer += "До конца пары: " + str(time)
                        break
                    if now < TIME['start'][e['number_pair']-1]:
                        time = TIME['start'][e['number_pair']-1] - now
                        timer += "До начала пары: " + str(time)
                        break

        s = todayKey + " " + weekday(datetime.datetime.now().weekday())  + "\n"
        for e in event_day:
            s += '\n'
            if pair_state == 1:
                s += str(e['number_pair']) + ") "
            if pair_time == 1:
                s += str(start[e['number_pair'] - 1]) + "-" + str(end[e['number_pair'] - 1]) + " "
            a = subject_full_name(subjects, e["subject_id"])
            if short_s == 1:
                a = subject_short_name(subjects, e["subject_id"])
            s += format_by_type(a, e['type'])
            s += " " + e['auditory'] + " "
            if len(e['teachers']) > 0:
                s += "\n"
                a = teacher_full_name(teachers, e['teachers'][0])
                if short_t == 1:
                    a = teacher_short_name(teachers, e['teachers'][0])
                s += a

        s += timer
        await bot.send_message(msg.from_user.id, s, parse_mode="HTML", reply_markup=kb_navigate)

@dp.message_handler(regexp="\A(1️⃣)\Z")
async def process_timetable1_command(msg: types.Message):
    register(msg)    
    await timetable(msg.from_user.id, 1)
    
@dp.message_handler(regexp="\A(7️⃣)\Z")
async def process_timetable7_command(msg: types.Message):
    register(msg)
    await timetable(msg.from_user.id, 7)

@dp.message_handler(regexp="\A(🔢)\Z")
async def process_timetable30_command(msg: types.Message):
    register(msg)
    await timetable(msg.from_user.id, 30)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await process_start_command(msg)

#region kb

btn_day_custom_schedule = KeyboardButton("🔀")
btn_day_schedule = KeyboardButton("1️⃣")
btn_week_schedule = KeyboardButton("7️⃣")
btn_month_schedule = KeyboardButton("🔢")
btn_home = KeyboardButton("🏠")
btn_settings = KeyboardButton("⚙️")
btn_info = KeyboardButton("🔍")
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start.row(btn_day_custom_schedule, btn_day_schedule, btn_week_schedule, btn_month_schedule)
kb_start.row(btn_home, btn_settings)

btn_gr = KeyboardButton("/gr")
btn_tn = KeyboardButton("/tn")
btn_sn = KeyboardButton("/sn")
kb_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_settings.insert(btn_gr)
kb_settings.insert(btn_tn)
kb_settings.insert(btn_sn)
kb_settings.insert(btn_home)
kb_settings.insert(btn_settings)
kb_settings.insert(btn_info)

kb_additional = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_additional.insert(btn_home)
kb_additional.insert(btn_settings)

#endregion

def pr1_poll():
    executor.start_polling(dp)

def pr2_updt():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    
    schedule.every().day.at("2:30").do(update_data)

    proc1 = Process(target=pr1_poll)
    proc2 = Process(target=pr2_updt)
    proc1.start()
    proc2.start()

