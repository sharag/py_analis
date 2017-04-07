"""Класс для работы с базой данных AIS"""
import sqlite3
import os


class AISdb:
    def __init__(self, db_fname):
        if not os.path.exists(db_fname):
            raise Exception('DB file not exist.')
        try:
            self.conn = sqlite3.connect(db_fname)
        except sqlite3:
            raise Exception('DB not connected.')
        self.num_mes = 0

    def add_msg(self, msg_):
        valcols = ":obj_pk, :channel, :msg_id, :mmsi, :routes_pk, :ship_lat, :ship_long, :time, :offset, :lat, " \
                  ":long, :alt, :speed, :rssi, :mes_str"
        values = msg_
        try:
            self.conn.execute(
                "INSERT INTO messages(" + valcols.replace(':', '') + ") VALUES (" + valcols + ");", values)
        except sqlite3 as err:
            print(err)
        if self.num_mes > 16:
            self.conn.commit()
            self.num_mes = 0

    """ select 
        field1,
        field2, 
        case
        when field1>0 then field1*5 
        end new_field
        from tabe1"""

    def get_slots(self, start, stop):
        """Для построения распределения mmsi по слотам"""
        query = "SELECT mmsi, offset FROM messages WHERE offset >= " + str(start) + " AND offset < " + str(stop) + ";"
        try:
            cursor = self.conn.execute(query)
        except BaseException as err:
            print('''SELECT mmsi, offset FROM messages WHERE offset >= ''' + str(start) + ''' AND offset < ''' +
                  str(stop) + ''';:''', err)
            raise BaseException(err)
        tab = []
        for row in cursor:
            if row[0] > 0:
                tab.append([row[0], row[1]])
        return tab

    def get_time(self):
        query = "SELECT time FROM messages;"
        try:
            cursor = self.conn.execute(query)
        except BaseException as err:
            print("SELECT time FROM messages;: ", err)
            raise BaseException(err)
        tab = []
        for row in cursor:
            if not row[0] in tab:
                tab.append(row[0])
        return tab

    def get_offset(self, time):
        query = "SELECT mmsi, offset FROM messages WHERE time = '" + time + "';"
        try:
            cursor = self.conn.execute(query)
        except BaseException as err:
            print("SELECT mmsi, offset FROM messages WHERE time = '" + time + "'; : ", err)
            raise BaseException(err)
        tab = []
        for row in cursor:
            if row[0] > 0:
                tab.append([row[0], row[1]])
        return tab

    def __del__(self):
        if self.conn is not None:
            print("Closing connection with DB.")
            self.conn.commit()
            self.conn.close()
