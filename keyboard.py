from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ContentType

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