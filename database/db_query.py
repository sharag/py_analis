'''
Created on 11 янв. 2017 г.

@author: xail
'''

#!/usr/bin/python3.5
import sqlite3
import os

class DbQuery:
    def __init__(self, f, main_win_ex):
        self.main_win_ex = main_win_ex
        if not os.path.isfile(f):
            raise BaseException('File ', f, ' does not exist')
            # Коннект к Базе
        try:
            self.connect_bd = sqlite3.connect(f)
        except BaseException as errcode2:
            print("Connect with DB failed: ", str(errcode2))
            self.main_win_ex.show_satus('Не удалось установить соединение с базой данных')
            raise BaseException("Connect with DB failed: ", str(errcode2))
        print("Connect with DB successful.\tOk.")
        self.main_win_ex.show_satus('Соединение с базой данных установлено')

    def get_objects(self):
        object_tab = []
        query = 'SELECT NAMEOBJ FROM OBJECTS;'
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get NAMEOBJ from table OBJECTS error: ", err)
            raise BaseException(err)
        for row in cursor:
            for val in row:
                object_tab.append(val)
        return object_tab

    def get_types(self, obj):
        type_tab = []
        query = "SELECT TYPE FROM OBJECTS WHERE NAMEOBJ = '" + obj + "';"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get TYPE from table OBJECTS error: ", err)
            raise BaseException(err)
        for row in cursor:
            for val in row:
                type_tab.append(val)
        return type_tab

    def get_subtypes(self, obj, type_):
        subtype_tab = []
        query = "SELECT SUBTYPE FROM OBJECTS WHERE NAMEOBJ = '" + obj + "' AND TYPE = '" + type_ + "';"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get SUBTYPE from table OBJECTS error: ", err)
            raise BaseException(err)
        for row in cursor:
            for val in row:
                subtype_tab.append(val)
        return subtype_tab

    def get_country(self, obj, type_, subtype):
        country_tab = []
        query = "SELECT COUNTRY FROM OBJECTS WHERE NAMEOBJ = '" + obj + "' AND TYPE = '" + type_ + "' AND SUBTYPE = '" + subtype + "';"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get COUNTRY from table OBJECTS error: ", err)
            raise BaseException(err)
        for row in cursor:
            for val in row:
                country_tab.append(val)
        return country_tab

    def get_rl(self, obj, type_, subtype, country):
        rl_tab = []
        query_obj = "SELECT OBJTYPEID FROM OBJECTS WHERE NAMEOBJ = '" + obj + "' AND TYPE = '" + type_ +\
                    "' AND SUBTYPE = '" + subtype + "' AND COUNTRY = '" + country + "'"
        query = "SELECT RLNAME FROM RL WHERE OBJTYPEID = (" + query_obj + ");"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get RLNAME from table RL error: ", err)
            raise BaseException(err)
        for row in cursor:
            for val in row:
                rl_tab.append(val)
        return rl_tab

    def get_main_frame(self, rl_name):
        main_frame_tab = []
        query_com = "SELECT COMMUTID FROM RL WHERE RLNAME = '" + rl_name + "'"
        query = "SELECT COMMUTID, CNAME, PARENT, FRBITLEN, WBITLEN, FREQFR, SIGNTYPE, WORDTABLE FROM COMMUTS WHERE COMMUTID = (" + query_com + ");"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get COMMUTID, CNAME, PARENT, FRBITLEN, WBITLEN, FREQFR, SIGNTYPE, WORDTABLE from table COMMUTS error: ", err)
            raise BaseException(err)
        for row in cursor:
            for val in row:
                main_frame_tab.append(val)
        main_frame_tab.append(self.get_markers(main_frame_tab[0]))
            
            
        return main_frame_tab
    
    def get_all_commuts(self, commut_id, commuts_tab):
        query = "SELECT COMMUTID, CNAME, PARENT, FRBITLEN, WBITLEN, FREQFR, SIGNTYPE, WORDTABLE FROM COMMUTS WHERE PARENT = " + str(commut_id) + ";"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get COMMUTID, CNAME, PARENT, FRBITLEN, WBITLEN, FREQFR, SIGNTYPE, WORDTABLE from table COMMUTS error: ", err)
            raise BaseException(err)
        for row in cursor:
            commuts_tab.append([])
            len_tab = len(commuts_tab)
            for val in row:
                commuts_tab[len_tab - 1].append(val)
            if len(commuts_tab[len_tab - 1][7]) > 0:
                name_wt = commuts_tab[len_tab - 1][7]
                del commuts_tab[len_tab - 1][7]
                commuts_tab[len_tab - 1].append(self.get_word_table(name_wt))
            self.get_all_commuts(commuts_tab[len_tab - 1][0], commuts_tab)
            commuts_tab[len_tab - 1].append(self.get_markers(commuts_tab[len_tab - 1][0]))
                
            
    def get_word_table(self, name_wt):
        wtab = []
        query = "SELECT * FROM " + name_wt + ";"
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get * from table " + name_wt + "error: ", err)
            raise BaseException(err)
        wordnum = 0
        for row in cursor:
            wtab.append([])
            wordnum += 1
            for val in row:
                wtab[wordnum - 1].append(val)
        return wtab
    
    def get_markers(self, commut_id):
        tab_markers  = []
        query = 'SELECT MARKERID, BITLEN, MVALUE, BITOFFSET FROM MARKERS WHERE COMMUTID = ' + str(commut_id) + ';'
        try:
            cursor = self.connect_bd.execute(query)
        except BaseException as err:
            print("Get MARKERID, BITLEN, MVALUE, BITOFFSET from table MARKERS error: ", err)
            raise BaseException(err)
        num_of_marker = 0
        for row in cursor:
            tab_markers.append([])  # Добавление вложенной ячейки для списка маркеров,
            # соответствующих COMMUTID
            for val in row:
                tab_markers[num_of_marker].append(val)
            num_of_marker += 1
        return tab_markers
            
    def __del__(self):
        self.connect_bd.close()
        