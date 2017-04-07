#!/usr/bin/python3.5
import argparse
import os
import sys
import glob
import datetime
import sqlite3
import aisparser


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
                "INSERT INTO messages(obj_pk, channel, msg_id, mmsi, routes_pk, ship_lat, ship_long, time, offset, lat,"
                " long, alt, speed, rssi, mes_str) VALUES (" + valcols + ");", values)
        except sqlite3 as err:
            print(err)
        if self.num_mes > 16:
            self.conn.commit()
            self.num_mes = 0

    def __del__(self):
        if self.conn is not None:
            print("Closing connection with DB.")
            self.conn.commit()
            self.conn.close()


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    return parser_


# s = ["!AIVDM,1,1,,B,35Mj3MPOj@o?FVFK<5w3r3@L00di,0*0F",
#     "!AIVDM,1,1,,B,11auciwP?w<tSF0l4Q@>4?wv0dBP,0*02",
#     "!AIVDM,1,1,,B,403OwpiuJo>A@o=sbvK=CG700H9n,0*33",
#     "!AIVDM,1,1,,B,35Mk33gOkRG?FLDK?6tUODNR0000,0*56",
#     "!AIVDM,2,1,2,B,8030ojA?0@=DE3@?BDPA3onQiUFttP1Wh01DE3<1EJ?>0onlkUG0e01I,0*3D",
#     "!AIVDM,2,2,2,B,h00,2*7D",
#     "!AIVDM,2,1,9,B,8030ojA?0@=DE3C?B5<00o`O1UA@V01vh01DE63>DB3?5oW@PU?d4P1i,0*55",
#     "!AIVDM,2,2,9,B,h00,2*76",
#     "!AIVDM,2,1,3,B,8030ojA?0@=DE9CD:?B9Fot`9UKQW03Gh01DE9CD6B19?oqHd5H=WP11,0*51",
#     "!AIVDM,2,2,3,B,h00,2*7C",
#     "\s:ASM//Port=63//MMSI=2573225,c:1301961602*7A\!BSVDM,1,1,,A,13P<JR50h00IkkJQi<Dt29ef0`PL,0*57"
#     ]


ais_state = aisparser.ais_state()

if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    inpath = namespace.inpath[0]
    if len(namespace.inpath) > 1:
        for i in range(1, len(namespace.inpath)):
            inpath += ' ' + namespace.inpath[i]
    namespace.inpath = inpath
    del inpath
    if os.path.exists(namespace.inpath) and os.path.isfile(namespace.inpath):
        filesList = [namespace.inpath]
    else:
        filesList = glob.glob(namespace.inpath + '*', recursive=False)
    if len(filesList) < 1:
        raise BaseException('In the catalog a little of files.')
    filesList.sort()
    numfile = 0

    db_ais = AISdb('/var/smbmount/extra/projects/aisparser/python/linux/ais_db.sqlite3')

    clear_dict_obj = {'mmsi': 0,
                      'name': '',
                      'dest': '',
                      'callsign': ''}
    clear_dict_msg = {'obj_pk': 0,
                      'channel': '',
                      'msg_id': 0,
                      'mmsi': 0,
                      'routes_pk': 0,
                      'ship_lat': 0.0,
                      'ship_long': 0.0,
                      'time': '',
                      'offset': 0.0,
                      'lat': 0.0,
                      'long': 0.0,
                      'alt': 0.0,
                      'speed': 0.0,
                      'rssi': 0.0,
                      'mes_str': ''}
    for fileName in filesList:
        numfile += 1
        text = ''
        fid_in = open(fileName, 'r')
        for line in fid_in:
            line = line.split('\t')
            # Если плохая строка
            if line[0].find('!') != 0:
                continue
            # Строка хороша
            result = aisparser.assemble_vdm(ais_state, line[0])
            if result:
                continue
            else:
                dict_msg = dict(clear_dict_msg)
                dict_obj = dict(clear_dict_obj)
                ais_state.msgid = aisparser.get_6bit(ais_state.six_state, 6)
                dict_msg['msg_id'] = ais_state.msgid
                dict_msg['channel'] = line[0].split(',')[4]
                if ais_state.msgid == 1:
                    msg = aisparser.aismsg_1()
                    aisparser.parse_ais_1(ais_state, msg)
                    (status, lat_dd, long_ddd) = aisparser.pos2ddd(msg.latitude, msg.longitude)
                    dict_msg['mmsi'] = msg.userid
                    dict_msg['ship_lat'] = lat_dd
                    dict_msg['ship_long'] = long_ddd
                elif ais_state.msgid == 2:
                    msg = aisparser.aismsg_2()
                    aisparser.parse_ais_2(ais_state, msg)
                    (status, lat_dd, long_ddd) = aisparser.pos2ddd(msg.latitude, msg.longitude)
                    dict_msg['mmsi'] = msg.userid
                    dict_msg['ship_lat'] = lat_dd
                    dict_msg['ship_long'] = long_ddd
                elif ais_state.msgid == 3:
                    msg = aisparser.aismsg_3()
                    aisparser.parse_ais_3(ais_state, msg)
                    (status, lat_dd, long_ddd) = aisparser.pos2ddd(msg.latitude, msg.longitude)
                    dict_msg['mmsi'] = msg.userid
                    dict_msg['ship_lat'] = lat_dd
                    dict_msg['ship_long'] = long_ddd
                elif ais_state.msgid == 4:
                    msg = aisparser.aismsg_4()
                    aisparser.parse_ais_4(ais_state, msg)
                    (status, lat_dd, long_ddd) = aisparser.pos2ddd(msg.latitude, msg.longitude)
                    dict_msg['mmsi'] = msg.userid
                    dict_msg['ship_lat'] = lat_dd
                    dict_msg['ship_long'] = long_ddd
                elif ais_state.msgid == 5:
                    msg = aisparser.aismsg_5()
                    aisparser.parse_ais_5(ais_state, msg)
                    dict_msg['mmsi'] = msg.userid
                else:
                    print('Unknown line. msg_id = ' + str(ais_state.msgid))
                dict_msg['mes_str'] = line[0]
            if len(line) > 3:
                date_ = line[1].split(', ')[0]
                time_ = line[1].split(', ')[1]
                dict_msg['time'] = datetime.datetime(year=int(date_.split('-')[2]),
                                                     month=int(date_.split('-')[1]),
                                                     day=int(date_.split('-')[0]),
                                                     hour=int(time_.split(':')[0]),
                                                     minute=int(time_.split(':')[1]))
                dict_msg['offset'] = float(time_.split(':')[2])
                dict_msg['rssi'] = float(line[2])
                str_gps = line[3].split(' ')
                dict_msg['lat'] = float(str_gps[0])
                dict_msg['long'] = float(str_gps[1])
                dict_msg['alt'] = float(str_gps[2])
                dict_msg['speed'] = float(str_gps[3])
            db_ais.add_msg(dict_msg)



