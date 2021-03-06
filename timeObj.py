import time
import datetime

def timeObj():
    end = list()
    start = list()
    now = datetime.datetime.now() + datetime.timedelta(hours=3)
    pairStart = now.strftime("%Y.%m.%d")
    pairStart = datetime.datetime.strptime(pairStart, "%Y.%m.%d")
    pairStart += datetime.timedelta(hours=7)
    pairStart += datetime.timedelta(minutes=45)
    pairEnd = pairStart + datetime.timedelta(hours=1) + datetime.timedelta(minutes=35)
    start.append(pairStart)
    end.append(pairEnd)

    for i in range(1,6):
        m = 10
        if i == 3:
            m = 20

        pairStart = pairEnd + datetime.timedelta(minutes=m)
        pairEnd = pairStart + datetime.timedelta(hours=1) + datetime.timedelta(minutes=35)
        start.append(pairStart)
        end.append(pairEnd)

    TIME = dict()
    TIME['start'] = start
    TIME['end'] = end
    return TIME

