from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import datetime
import time
import urllib3
import json
from time import sleep
from id import subject_full_name, subject_short_name, teacher_full_name, teacher_short_name
from config import TOKEN, MY_ID, StatesGroup
from groups import DATA
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

def register(msg):
    with conn:
        c.execute("SELECT * FROM users WHERE id=:id", {'id':msg.from_user.id})
        i = datetime.datetime.now()
        if len(list(c.fetchall())) == 0:
            c.execute("INSERT INTO users VALUES (:id, :name, 1, 1, :f_n, :g_n, -1, :date, :updates, :state)",
             {'id':msg.from_user.id, 'name':msg.from_user.full_name, "updates": 1,
             "date": "%s" % i, 'state': StatesGroup.S_NONE.value, 'f_n': "", "g_n": ""})
        else:
            c.execute("UPDATE users SET last_update=:date WHERE id=:id",{'id': msg.from_user.id, 'date': "%s" % i})
            c.execute("SELECT * FROM users WHERE id=:id", {'id': msg.from_user.id})
            obj = c.fetchone()
            num = obj[8] + 1
            c.execute("UPDATE users SET updates=:upd WHERE id=:id", {'id': msg.from_user.id, 'upd': num})
            
def set_state(id, num):
    with conn:
        c.execute("UPDATE users SET grp_state = :state WHERE id = :id", {'id': id, "state" : num})

def get_state(id):
    with conn:
        c.execute("SELECT * FROM users WHERE id = :id", {'id': id})
        obj = c.fetchone()
        return obj[9]

def boolChange(id, key):
    with conn:
        c.execute("SELECT * FROM users WHERE id=:id", {'id':id})
        user = c.fetchone()
        if key == "short_teacher":
            n = 3
        else:
            n = 2
        val = 1
        if user[n] == 1:
            val = 0
        c.execute("UPDATE users SET " + key + " = :val WHERE id=:id""", {'id':id, 'val':val})

async def timetable(id, num):
    short_t = 0
    short_s = 0
    group_id = 0
    with conn:
        c.execute("SELECT * FROM users WHERE id = :id", {'id':id})
        user = c.fetchone()
        short_t = user[3]
        short_s = user[2]
        group_id = user[6]
        if user[6] == -1:
            await bot.send_message(id, "Не указана группа", reply_markup=kb_additional)
            return

    s_start = datetime.datetime.now()
    if s_start.hour >= 18 and s_start.minute >= 15:
        s_start += datetime.timedelta(days=1)
    s_end = s_start + datetime.timedelta(days=num - 1)

    d_start = s_start.strftime("%Y-%m-%d")
    d_end = s_end.strftime("%Y-%m-%d")

    t_start = time.strptime(d_start, '%Y-%m-%d')
    t_end = time.strptime(d_end, '%Y-%m-%d')
    
    ep_start = int(time.mktime(t_start))
    ep_end = int(time.mktime(t_end))
    
    url = "http://cist.nure.ua/ias/app/tt/P_API_EVEN_JSON?timetable_id=" + str(group_id) + "&type_id=1&time_from=" + str(ep_start) + "&time_to=" + str(ep_end)
    http = urllib3.PoolManager()
    
    r = http.request('GET', url)
    obj = dict()
    try:
        obj = json.loads(r.data.decode('cp1251'))
    except:
        await bot.send_message(id, "Пар не найдено", reply_markup=kb_additional)
        return
        
    event_day = dict()
    start = ['7:45', "9:30", "11:15", "13:10", "14:55", "16:40"]
    end = ['9:20', "11:05", "12:50", "14:45", "16:30", "18:15"]

    for event in obj['events']:
        key = time.strftime("%d.%m.%Y", time.localtime(event["start_time"]))
        try:
            event_day[key].append(event)
        except:
            event_day[key] = list()
            event_day[key].append(event)

    if len(event_day) == 0:
        print("Пар не найдено")
        return

    for k in event_day:
        s = k
        for e in event_day[k]:
            s += '\n'
            s += "[" + str(start[e['number_pair'] - 1]) + "-" + str(end[e['number_pair'] - 1]) + "] " + "[" + e['auditory'] + "] "
            a = subject_full_name(obj, e["subject_id"])
            if short_t == 1:
                a = subject_short_name(obj, e["subject_id"])
            s += a
            if len(e['teachers']) > 0:
                s += "\n"
                a = teacher_full_name(obj, e['teachers'][0])
                if short_t == 1:
                    a = teacher_short_name(obj, e['teachers'][0])
                s += a
                
        await bot.send_message(id, s, reply_markup=kb_additional)
        time.sleep(0.3)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect('user.db')
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
    data = eval(call.data)
    faculty = DATA['university']['faculties'][data['f']]
    direction = faculty['directions'][data['d']]
    group = direction['groups'][data['g']]
    with conn:
        c.execute("UPDATE users SET group_id = :upd, group_name = :g_n, faculty_name = :f_n WHERE id=:id",
        {'upd': group['id'], 'id': call.message.chat.id, 'g_n': group['name'], 'f_n': faculty['full_name']})
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Изменения вступили в силу")        

@dp.callback_query_handler()
async def process_callback_button1(call: types.CallbackQuery):
    faculty = call.data
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Факультет: {}\n\n Специальность:".format(faculty))

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    register(message)
    set_state(message.from_user.id, StatesGroup.S_NONE.value)
    #if message.from_user.id == MY_ID:
    await bot.send_message(message.from_user.id, "Расписание\n\n1️⃣ — На 1 день\n7️⃣ — На 7 дней\n🔢 — На 30 дней\n\n 🏠 — Стартовая страница /start\n ⚙️ — Настройки /settings", reply_markup=kb_start)

@dp.message_handler(commands=['db'])
async def process_db_command(message: types.Message):
    with conn:
        c.execute("SELECT * FROM users")
        lst = c.fetchall()
        for data in lst:
            await bot.send_message(message.from_user.id, data)

@dp.message_handler(commands=["tn"])
async def teacher_name_change(msg: types.Message):
    boolChange(msg.from_user.id, "short_teacher")
    await process_settings_command(msg)

@dp.message_handler(commands=["sn"])
async def subject_name_change(msg: types.Message):
    boolChange(msg.from_user.id, "short_subj")
    await process_settings_command(msg)

@dp.message_handler(regexp="\A(⚙️)\Z")
async def process_emoji_settings_command(msg: types.Message):
    await process_settings_command(msg)

@dp.message_handler(commands=['settings'])
async def process_settings_command(msg: types.Message):
    set_state(msg.from_user.id, StatesGroup.S_NONE.value)
    with conn:
            c.execute("SELECT * FROM users WHERE id=:id", {'id':msg.from_user.id})
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
            string = "Настройки\n\n"
            string += "Группа: {} /gr\n".format(group)
            string += "Полные имена предметов: {} /sn\n".format(full_s)
            string += "Полные имена преподавателей: {} /tn\n".format(full_t)
            string += "\n"
            string += "🔍 Справка /help"

            #if msg.from_user.id == MY_ID:
            await bot.send_message(msg.from_user.id, string, reply_markup=kb_settings)

@dp.message_handler(commands=['help'])
async def process_info_command(msg: types.Message):
    set_state(msg.from_user.id, StatesGroup.S_NONE.value)
    s = "Расписание на день работает выдачей записей до конца дня. "
    s += "Если время вызова позднее 18:15, команда обработает записи на завтра. "
    s += "Для недели и месяца аналогично"
    # s += "\n\n"
    # s += "Планы на будущее: напоминания, таймер до конца пары, расписание для преподавателя, фильтр предметов.\n"
    # s += "Автор не претендует на оригинальность или конкуренцию с более ранними приложениями"
    s += "\n\n"
    s += "Разработчик: @VledSh"
    await bot.send_message(msg.from_user.id, s, reply_markup=kb_additional)

@dp.message_handler(regexp="\A(🔍)\Z")
async def process_info_emoji_command(msg: types.Message):
    await process_info_command(msg)

@dp.message_handler(regexp="\A(1️⃣)\Z")
async def process_timetable1_command(msg: types.Message):
    await timetable(msg.from_user.id, 1)

@dp.message_handler(regexp="\A(7️⃣)\Z")
async def process_timetable7_command(msg: types.Message):
    await timetable(msg.from_user.id, 7)

@dp.message_handler(regexp="\A(🔢)\Z")
async def process_timetable30_command(msg: types.Message):
    await timetable(msg.from_user.id, 30)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await process_start_command(msg)


btn_day_schedule = KeyboardButton("1️⃣")
btn_week_schedule = KeyboardButton("7️⃣")
btn_month_schedule = KeyboardButton("🔢")
btn_home = KeyboardButton("🏠")
btn_settings = KeyboardButton("⚙️")
btn_info = KeyboardButton("🔍")
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start.insert(btn_day_schedule)
kb_start.insert(btn_week_schedule)
kb_start.insert(btn_month_schedule)
kb_start.insert(btn_home)
kb_start.insert(btn_settings)

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

kb_additional = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_additional.insert(btn_home)
kb_additional.insert(btn_settings)

if __name__ == '__main__':
    executor.start_polling(dp)
