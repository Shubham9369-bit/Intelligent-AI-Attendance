import sqlite3
import pandas as pd
from contextlib import closing
from datetime import datetime

DB = "attendance.db"

def _conn():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, date TEXT NOT NULL, time TEXT NOT NULL,
        UNIQUE(name, date))""")
    return c

def mark(name, d=None, t=None):
    now = datetime.now()
    d = d or str(now.date())
    t = t or now.strftime("%H:%M:%S")
    with closing(_conn()) as c:
        c.execute("INSERT OR IGNORE INTO attendance(name,date,time) VALUES(?,?,?)",
                  (name, d, t))
        c.commit()

def get_all():
    with closing(_conn()) as c:
        return pd.read_sql_query(
            "SELECT name AS Name, date AS Date, time AS Time FROM attendance ORDER BY id", c)

def get_day(d):
    with closing(_conn()) as c:
        return pd.read_sql_query(
            "SELECT name AS Name, date AS Date, time AS Time FROM attendance WHERE date=?",
            c, params=(str(d),))