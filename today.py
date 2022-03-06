import time

import urllib.request
import json
from datetime import datetime
from dateutil import parser

link = "https://public.mai.ru/schedule/data/bdc71a9a967c1e24f6e55a208f452202.json"
rasp = urllib.request.urlopen(link).read()
rasp = json.loads(rasp)

rasp.pop("group")

group_rasp = []

for day in rasp.items():
    date = datetime.fromisoformat(str(parser.parse(day[0], dayfirst=True)))
    # print(date.date())
    pary = day[1]["pairs"]

    for _para in pary.items():
        para = _para[1]
        
        time_start = datetime.fromisoformat(
            str(parser.parse(para["time_start"])))
        time_start = datetime.combine(date.date(), time_start.time())
        time_end = datetime.fromisoformat(str(parser.parse(para["time_end"])))
        time_end = datetime.combine(date.date(), time_end.time())

        name = []
        for _name in para["class"].items():
            name.append(_name[0])
        name = ' / '.join(name)

        lector = []
        for _lector in para["lector"].items():
            lector.append(_lector[1])
        lector = ', '.join(lector)

        type = []
        for _type in para["type"].items():
            type = _type[0]

        room = []
        for _room in para["room"].items():
            room.append(_room[1])
        room = ', '.join(room)
        
        if time.localtime().tm_mday + 1 == time_start.day and time.localtime().tm_mon == time_start.month and time_start.year == time.localtime().tm_year:
        
            group_rasp.append({"time_start": time_start.ctime(), "time_end": time_end.ctime(
        ), "name": name, "type": type, "lector": lector, "room": room})
print(group_rasp)