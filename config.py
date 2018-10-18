from enum import Enum

TOKEN = ""
MY_ID = 0
SOURCE = "https://github.com/VladShg/nure-telegram-bot"

class StatesGroup(Enum):

    S_NONE = 1 
    S_ENTER_FAC = 2
    S_ENTER_DIR = 3
    S_ENTER_GROUP = 4
