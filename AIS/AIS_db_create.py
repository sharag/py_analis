# !/usr/bin/python3.5

import argparse
import sqlite3
import datetime
import os


# import time
# import sys


def create_tables(out_db_name):
    if os.path.isfile(out_db_name):
        os.remove(out_db_name)

    conn_bd = sqlite3.connect(out_db_name)
    print("Database created  successfully")

    # Таблица с сообщениями
    conn_bd.execute('''CREATE TABLE messages (
    mes_pk    INTEGER PRIMARY KEY ASC AUTOINCREMENT NOT NULL,
    obj_pk    INTEGER,
    channel   VARCHAR (1),
    msg_id    INTEGER,
    mmsi      BIGINT,
    routes_pk INTEGER,
    ship_lat  DOUBLE,
    ship_long DOUBLE,
    time      DATETIME,
    [offset]  DOUBLE,
    lat       DOUBLE,
    long      DOUBLE,
    alt       DOUBLE,
    speed     DOUBLE,
    rssi      DOUBLE,
    mes_str   VARCHAR (200) );''')

    conn_bd.commit()
    conn_bd.close()
    print("Tables created successfully")


def main():
    outbase = '//FS37/extra/projects/aisparser/python/linux/ais_db.sqlite3'
    print("Creating tables in ", outbase, "...")
    create_tables(outbase)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting on SIGINT")
    except BaseException as e:
        print("Exiting on exception: " + str(e))
    else:
        print("Exiting on connection loss")