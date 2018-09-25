from enum import Enum

TOKEN = "677779116:AAGfKJSZqvsb-qTVXVR3rzYx2rST0MOw6h0"
MY_ID = 108458898
SOURCE = "https://github.com/VladShg/nure-telegram-bot"

class StatesGroup(Enum):

    S_NONE = 1 
    S_ENTER_FAC = 2
    S_ENTER_DIR = 3
    S_ENTER_GROUP = 4
