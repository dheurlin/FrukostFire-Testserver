import sqlite3
import json

from typing import Dict

conn = sqlite3.connect('/data/database.db', check_same_thread=False)

conn.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        name     VARCHAR    PRIMARY KEY
      , gnall    VARCHAR
    ) ;
""")

def insert_attendent(name: str, gnäll: Dict[str, str]) -> None:
    gnällson = json.dumps(gnäll)
    with conn:
        conn.execute("INSERT INTO applications (name, gnall) values (?, ?) ", (name, gnällson))

