from datetime import timedelta
import sqlite3

total = 0


def sub(item):
    start, end = item
    return end - start


def get_time():
    with sqlite3.connect('ActivityRecords.db') as db:
        query = db.execute("SELECT * FROM ACTIVITY")
        mapped_data = map(sub, query)
    total_time = sum(mapped_data)
    return timedelta(seconds=total_time)


if __name__ == '__main__':
    print(get_time())