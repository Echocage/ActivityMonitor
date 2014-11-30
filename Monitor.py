import configparser
import datetime
import re
import time
import sqlite3

from pyxhook import HookManager
from xdotool import get_active_window


with sqlite3.connect('ActivityRecords.db') as db:
    db.execute("CREATE TABLE IF NOT EXISTS activity(start INT,end INT)")
    db.commit()

config = configparser.ConfigParser({'main': '.*'})
config.read('config')
is_target = re.compile(config.get('main', 'regex_window_title'), re.IGNORECASE)

last_active = 0

def event_handler(event):
    global last_active
    now = time.time()
    if time.time() > last_active + datetime.timedelta(seconds=30).total_seconds():
        active_window = get_active_window()
        matches_regex = is_target.search(active_window)
        if matches_regex:
            last_active = time.time()
            with sqlite3.connect("ActivityRecords.db") as db:
                results = db.execute("UPDATE activity SET end = ? WHERE end > ?",
                                     (now, now - datetime.timedelta(minutes=5).total_seconds())).rowcount
                if not results:
                    db.execute('INSERT INTO activity VALUES (?,?)', (now, now))
                db.commit()


if __name__ == '__main__':
    hm = HookManager()
    hm.HookKeyboard()
    hm.HookMouse()
    hm.KeyDown = event_handler
    hm.MouseAllButtonsDown = event_handler
    hm.start()
