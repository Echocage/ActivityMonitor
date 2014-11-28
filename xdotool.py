import os

import time
import sys


def click(click_number=1):
    return _execute('xdotool click ' + click_number)


def _get_active_window():
    return _execute('xdotool getActiveWindow')


def get_active_window():
    return _execute('xdotool getWindowName ' + _get_active_window()).strip()


def get_mouse_location():
    x, y = _execute('xdotool getmouselocation --shell').split()[:2]
    return x.split('=')[1], y.split('=')[1]


def _execute(args):
    with os.popen(args) as executor:
        return executor.read()


if 'Available commands' not in _execute("xdotool"):
    print('xdotool required for function, stopping...')
    sys.exit()

if __name__ == '__main__':
    times = list()
    for x in range(100):
        start = time.time()
        get_active_window()
        end = time.time()
        times.append(end - start)
    print(len(times) / sum(times))