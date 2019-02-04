import sqlite3
from typing import List

conn = sqlite3.connect('/data/database.db', check_same_thread=False)

conn.execute("""
    CREATE TABLE IF NOT EXISTS attendant (
        name TEXT PRIMARY KEY
    ) ;
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS gnäll (
        name TEXT PRIMARY KEY
    ) ;
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS attendant_gnäll (
        attendant_name TEXT REFERENCES attendant(name)
      , gnäll_name     TEXT REFERENCES gnäll(name)
    ) ;
""")

def insert_attendent(name: str, gnäll: List[str]) -> None:
    gnälls    = map(lambda g: (g,)    , gnäll)
    namngnäll = map(lambda g: (name,g), gnäll)
    with conn:
        conn.execute    ("INSERT           INTO attendant (name) VALUES (?) ", (name ,))
        conn.executemany("INSERT OR IGNORE INTO gnäll     (name) VALUES (?) ", gnälls  )

        conn.executemany("""
            INSERT into attendant_gnäll (attendant_name, gnäll_name)
            VALUES (?,?)
         """,  namngnäll)


# HOW to select: https://stackoverflow.com/questions/7296846/how-to-implement-one-to-one-one-to-many-and-many-to-many-relationships-while-de
