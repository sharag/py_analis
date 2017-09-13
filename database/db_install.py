'''
Created on 11 янв. 2017 г.

@author: xail
'''

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

    # Таблица с видами модуляции
    conn_bd.execute("CREATE TABLE MODULATION(MTYPEID INTEGER PRIMARY KEY, MNAME VARCHAR(64));")

    # Таблица с типами объектов
    conn_bd.execute('''CREATE TABLE OBJECTS    (
    OBJTYPEID INTEGER PRIMARY KEY, 
    NAMEOBJ VARCHAR(64),
    TYPE VARCHAR(64),
    SUBTYPE VARCHAR(64), 
    COUNTRY VARCHAR(64));''')

    # Таблица с типами радиолиний
    conn_bd.execute('''CREATE TABLE RL (
    RLTYPEID INTEGER PRIMARY KEY, 
    RLNAME VARCHAR(64), 
    OBJTYPEID INTEGER, 
    MTYPEID INTEGER, 
    SRATE NUMERIC, 
    DELTAF NUMERIC, 
    COMMUTID INTEGER,
    SCRAMBLERID INTEGER,
    FECOUTID INTEGER,
    INTERLEAVERID INTEGER,
    FECINID INTEGER,
    MANCODINGID INTEGER,
    PCKTTYPE INTEGER);''')

    # Таблица с видами маркеров
    conn_bd.execute('''CREATE TABLE MARKERS (
    MARKERID INTEGER PRIMARY KEY,
    COMMUTID INTEGER,
    BITLEN INTEGER,
    MVALUE VARCHAR(32),
    BITOFFSET INTEGER);''')

    # Таблица с типами коммутаторов
    conn_bd.execute('''CREATE TABLE COMMUTS (
    COMMUTID INTEGER PRIMARY KEY,
    CNAME VARCHAR(32),
    PARENT INTEGER,
    FRBITLEN INTEGER,
    WBITLEN INTEGER,
    FREQFR INTEGER,
    SIGNTYPE VARCHAR(64),
    WORDTABLE VARCHAR(32));''')

    # Таблица с описаниями каналов для демультиплексора
#     conn_bd.execute('''CREATE TABLE CHANELS (
#     CHANID INTEGER PRIMARY KEY,
#     CHANNAME VARCHAR(32),
#     WBITLEN INTEGER,
#     COMMUTID INTEGER,
#     POS INTEGER);''')

    # Таблица с типами данных
    conn_bd.execute('''CREATE TABLE DATATYPE (
    DATATYPEID INTEGER PRIMARY KEY,
    TYPENAME VARCHAR(32));''')

    # Таблица с описаниями ТМП (как извлекать)
#     conn_bd.execute('''CREATE TABLE TMP (
#     TMPID INTEGER PRIMARY KEY,
#     TMPNAME VARCHAR(64),
#     CHANID INTEGER,
#     MASK VARCHAR(16),
#     TMPBITLEN INTEGER,
#     DATATYPEID INTEGER);''')

    conn_bd.execute('''CREATE TABLE SCRAMBLER (
    SCRAMBLERID INTEGER PRIMARY KEY,
    SCRAMBLERNAME VARCHAR(64),
    ADDTYPE BOOLEAN,
    INITSET VARCHAR(32),
    LFSR VARCHAR(32));''')

    conn_bd.execute('''CREATE TABLE FECOUT (
    FECOUTID INTEGER PRIMARY KEY,
    FECOUTNAME VARCHAR(64));''')

    conn_bd.execute('''CREATE TABLE INTERLEAVER (
    INTERLEAVERID INTEGER PRIMARY KEY,
    INTERLEAVERNAME VARCHAR(64));''')

    conn_bd.execute('''CREATE TABLE FECIN (
    FECINID INTEGER PRIMARY KEY,
    FECINNAME VARCHAR(64));''')

    conn_bd.execute('''CREATE TABLE MANCODING (
    MANCODINGID INTEGER PRIMARY KEY,
    MANCODINGNAME VARCHAR(64));''')

    # Таблица с описаниями запусков
    conn_bd.execute('''CREATE TABLE LAUNCH(
    LAUNCHID INTEGER PRIMARY KEY,
    LAUNCHTIME DATETIME,
    OBJTYPEID INTEGER,
    RLTYPEID INTEGER,
    FREQVALUE NUMERIC,
    LAUNCHMARKERS VARCHAR(32),
    ANALISRES VARCHAR(32));''')

    # Пример таблицы с перечнем использованных маркеров основного коммутатора
    conn_bd.execute('''CREATE TABLE MLAUNCH22_02_2012_1(
    MCOUNTID INTEGER PRIMARY KEY,
    MARKERID INTEGER);''')

    # Таблица со словами TR2NEW2012_D_D1
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_D1(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    # Таблица со словами TR2NEW2012_D_D2
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_D2(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    # Таблица со словами TR2NEW2012_D_D3
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_D3(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    # Таблица со словами TR2NEW2012_D_D4
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_D4(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    # Таблица со словами TR2NEW2012_D_D5
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_D5(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    # Таблица со словами TR2NEW2012_D_A
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_A(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    # Таблица со словами TR2NEW2012_D_D4_mode
    conn_bd.execute('''CREATE TABLE WT_TR2NEW2012_D_D4_mode(
    WORDID INTEGER PRIMARY KEY,
    BITPOSINPARENT INTEGER,
    WBITLEN INTEGER);''')

    conn_bd.commit()
    conn_bd.close()
    print("Tables created successfully")


def populate_bdtlm(out_db_name):
    conn_bd = sqlite3.connect(out_db_name)

    # Table OBJECTS

    # OBJTYPEID INTEGER PRIMARY KEY
    # NAMEOBJ VARCHAR(64)
    # TYPE VARCHAR(64)
    # SUBTYPE VARCHAR(64)
    # COUNTRY VARCHAR(64)
    conn_bd.execute("INSERT INTO OBJECTS VALUES(1,'TR2','ГЧ','АБР','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(2,'TR2','ГЧ','АБР','Великобритания');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(3,'TR2','БГ','БГ_А','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(4,'TR2','БГ','БГ_Б','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(5,'TR2','БГ','БГ_В','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(6,'TR2','БГ','БГ_Г','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(7,'TR2','БГ','БГ_Д','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(8,'TR2','БГ','БГ_Е','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(9,'TR2','БГ','БГ_Ж','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(10,'TR2','БГ','БГ_З','США');")
    conn_bd.execute("INSERT INTO OBJECTS VALUES(11,'TR2','БГ','БГ_И','США');")

    ################################################################################
    # Table MODULATION

    # MTYPEID INTEGER PRIMARY KEY
    # MNAME VARCHAR(64)
    conn_bd.execute("INSERT INTO MODULATION VALUES(1,'ЧМн');")
    conn_bd.execute("INSERT INTO MODULATION VALUES(2,'ФМ2');")
    conn_bd.execute("INSERT INTO MODULATION VALUES(3,'ФМ4');")
    conn_bd.execute("INSERT INTO MODULATION VALUES(4,'ФМ8');")
    conn_bd.execute("INSERT INTO MODULATION VALUES(5,'КИМ-ЧМ');")
    conn_bd.execute("INSERT INTO MODULATION VALUES(6,'КИМ-ФМ');")

    ################################################################################
    # Table RL

    # RLTYPEID INTEGER PRIMARY KEY
    # RLNAME VARCHAR(64)
    # OBJTYPEID INTEGER
    # MTYPEID INTEGER
    # SRATE NUMERIC
    # DELTAF NUMERIC
    # COMMUTID INTEGER
    # SCRAMBLERID INTEGER
    # FECOUTID INTEGER
    # INTERLEAVERID INTEGER
    # FECINID INTEGER
    # MANCODINGID INTEGER
    # PCKTTYPE INTEGER
    conn_bd.execute("INSERT INTO RL VALUES(1,'TR2NEW2012_D-LINE',1,5,1468800,1800000,1,0,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(2,'TR2NEW2012_A-LINE',1,5,1152000,1400000,2,0,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(3,'TR2NEW2012_БГ_А',3,5,768000,1000000,3,0,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(4,'TR2NEW2012_БГ_Б',4,5,786432,1000000,4,1,0,0,0,2,0);")
    conn_bd.execute("INSERT INTO RL VALUES(5,'TR2NEW2012_БГ_В',5,5,2333330,3000000,5,1,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(6,'TR2NEW2012_БГ_Г',6,5,800000,1000000,6,1,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(7,'TR2NEW2012_БГ_Д',7,5,400000,500000,7,0,0,0,0,2,0);")
    conn_bd.execute("INSERT INTO RL VALUES(8,'TR2NEW2012_БГ_Е',8,5,786432,1000000,8,0,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(9,'TR2NEW2012_БГ_Ж',9,5,786432,1000000,9,0,0,0,0,2,0);")
    conn_bd.execute("INSERT INTO RL VALUES(10,'TR2NEW2012_БГ_З',10,5,400000,500000,10,1,0,0,0,2,0);")
    conn_bd.execute("INSERT INTO RL VALUES(11,'TR2NEW2012_БГ_И',11,5,800000,1000000,11,1,0,0,0,2,0);")
    conn_bd.execute("INSERT INTO RL VALUES(12,'TR2NEW2012_D-LINE_BR',2,5,1468800,1800000,1,0,0,0,0,1,0);")
    conn_bd.execute("INSERT INTO RL VALUES(13,'TR2NEW2012_A-LINE_BR',2,5,1152000,1400000,2,0,0,0,0,1,0);")

    ################################################################################
    # Table COMMUTS

    # COMMUTID INTEGER PRIMARY KEY
    # CNAME VARCHAR(32)
    # PARENT INTEGER
    # FRBITLEN INTEGER
    # WBITLEN INTEGER
    # FREQFR INTEGER,
    # WORDTABLE VARCHAR(32)
    conn_bd.execute("INSERT INTO COMMUTS VALUES(1,'TR2NEW2012_D',0,14688,8,100,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(2,'TR2NEW2012_A',0,2880,8,400,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(3,'TR2NEW2012_БГ_А',0,3072,8,250,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(4,'TR2NEW2012_БГ_Б',0,1536,8,512,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(5,'TR2NEW2012_БГ_В',0,960,8,24301,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(6,'TR2NEW2012_БГ_Г',0,1600,8,500,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(7,'TR2NEW2012_БГ_Д',0,800,8,500,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(8,'TR2NEW2012_БГ_Е',0,3072,8,256,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(9,'TR2NEW2012_БГ_Ж',0,3072,8,256,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(10,'TR2NEW2012_БГ_З',0,800,8,500,'Основной','');")
    conn_bd.execute("INSERT INTO COMMUTS VALUES(11,'TR2NEW2012_БГ_И',0,1600,8,500,'Основной','');")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(12,'TR2NEW2012_D_D1',1,2448,16,100,'Субкоммутатор',
    'WT_TR2NEW2012_D_D1');""")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(13,'TR2NEW2012_D_D2',1,2448,16,100,'Субкоммутатор',
    'WT_TR2NEW2012_D_D2');""")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(14,'TR2NEW2012_D_D3',1,2448,16,100,'Субкоммутатор',
    'WT_TR2NEW2012_D_D3');""")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(15,'TR2NEW2012_D_D4',1,2448,16,100,'Субкоммутатор',
    'WT_TR2NEW2012_D_D4');""")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(16,'TR2NEW2012_D_D5',1,2368,16,100,'Субкоммутатор',
    'WT_TR2NEW2012_D_D5');""")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(17,'TR2NEW2012_D_A',1,2400,8,100,'Субкоммутатор',
    'WT_TR2NEW2012_D_A');""")
    conn_bd.execute("""INSERT INTO COMMUTS VALUES(18,'TR2NEW2012_D_D4_mode',15,16,16,100,'ТМП',
    'WT_TR2NEW2012_D_D4_mode');""")

    ################################################################################
    # Table MARKERS

    # MARKERID INTEGER PRIMARY KEY
    # COMMUTID INTEGER
    # BITLEN INTEGER
    # MVALUE VARCHAR(32)
    # BITOFFSET INTEGER
    conn_bd.execute("INSERT INTO MARKERS VALUES(1,1,32,'FAF33400',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(2,1,32,'FAF33401',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(3,1,32,'FAF33402',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(4,1,32,'FAF33403',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(5,1,32,'00B33D7C',4896);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(6,1,32,'00B33D7D',4896);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(7,1,32,'00B33D7E',4896);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(8,1,32,'00B33D7F',4896);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(9,1,32,'00B33D7C',9792);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(10,2,24,'0DB573',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(11,3,32,'FE6B2840',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(12,4,24,'FAF320',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(13,5,24,'FAF320',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(14,6,24,'FAF320',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(15,7,24,'FAF320',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(16,8,32,'FE6B2840',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(17,9,32,'FE6B2840',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(18,10,24,'FAF320',0);")
    conn_bd.execute("INSERT INTO MARKERS VALUES(19,11,24,'FAF320',0);")

    ################################################################################
    # Table SCRAMBLER

    # SCRAMBLERID INTEGER PRIMARY KEY
    # SCRAMBLERNAME VARCHAR(64)
    # ADDTYPE BOOLEAN
    # INITSET VARCHAR(32)
    # LFSR VARCHAR(32)
    conn_bd.execute("INSERT INTO SCRAMBLER VALUES(1,'Мультипликативный (14,15)',0,0,'14,15');")

    ################################################################################
    # Table FECOUT

    # FECOUTID INTEGER PRIMARY KEY
    # FECOUTNAME VARCHAR(64)
    conn_bd.execute("INSERT INTO FECOUT VALUES(1,'RS(255,238)');")

    ################################################################################
    # Table INTERLEAVER

    # INTERLEAVERID INTEGER PRIMARY KEY
    # INTERLEAVERNAME VARCHAR(64)
    conn_bd.execute("INSERT INTO INTERLEAVER VALUES(1,'Сверточный()');")

    ################################################################################
    # Table FECIN

    # FECINID INTEGER PRIMARY KEY
    # FECINNAME VARCHAR(64)
    conn_bd.execute("INSERT INTO FECIN VALUES(1,'NSK 1/2 (171,133)');")

    ################################################################################
    # Table MANCODING

    # MANCODINGID INTEGER PRIMARY KEY
    # MANCODINGNAME VARCHAR(32)
    conn_bd.execute("INSERT INTO MANCODING VALUES(1,'NRZ-L');")
    conn_bd.execute("INSERT INTO MANCODING VALUES(2,'RNRZ-L');")

    ################################################################################
    # Table LAUNCH

    # LAUNCHID INTEGER PRIMARY KEY
    # LAUNCHTIME DATETIME
    # OBJTYPEID INTEGER
    # RLTYPEID INTEGER
    # FREQVALUE NUMERIC
    # LAUNCHMARKERS VARCHAR(32)
    # ANALISRES VARCHAR(32))
    conn_bd.execute("INSERT INTO LAUNCH VALUES(1,?,1,1,2210500000,'MLAUNCH22_02_2012_1','');",
                    (datetime.datetime(2012, 2, 22, 18, 5, 3, 0),))

    ################################################################################
    # Пример таблицы с перечнем использованных маркеров основного коммутатора
    # Table MLAUNCH22_02_2012_1

    # MCOUNTID INTEGER PRIMARY KEY
    # MARKERID INTEGER
    conn_bd.execute("INSERT INTO MLAUNCH22_02_2012_1 VALUES(1,3);")
    conn_bd.execute("INSERT INTO MLAUNCH22_02_2012_1 VALUES(2,5);")
    conn_bd.execute("INSERT INTO MLAUNCH22_02_2012_1 VALUES(3,9);")

    ################################################################################
    # Таблица со словами TR2NEW2012_D_D1

    # Table WT_TR2NEW2012_D_D1
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    # Каждое 16-ти разрядное слово разбивается на 2 8-разрядных части. Части меняем местами
    numword = 153  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 32  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D1 VALUES(?,?,?);", (i*2 + 1, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D1 VALUES(?,?,?);", (i*2 + 2, start_pos + step*i, wbitlen))

    ################################################################################
    # Таблица со словами TR2NEW2012_D_D2

    # Table WT_TR2NEW2012_D_D2
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    # Каждое 16-ти разрядное слово разбивается на 2 8-разрядных части. Части меняем местами
    numword = 153  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 48  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D2 VALUES(?,?,?);", (i*2 + 1, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D2 VALUES(?,?,?);", (i*2 + 2, start_pos + step*i, wbitlen))

    ################################################################################
    # Таблица со словами TR2NEW2012_D_D3

    # Table WT_TR2NEW2012_D_D3
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    # Каждое 16-ти разрядное слово разбивается на 2 8-разрядных части. Части меняем местами
    numword = 153  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 64  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D3 VALUES(?,?,?);", (i*2 + 1, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D3 VALUES(?,?,?);", (i*2 + 2, start_pos + step*i, wbitlen))

    ################################################################################
    # Таблица со словами TR2NEW2012_D_D4

    # Table WT_TR2NEW2012_D_D4
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    # Каждое 16-ти разрядное слово разбивается на 2 8-разрядных части. Части меняем местами
    numword = 153  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 80  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D4 VALUES(?,?,?);", (i*2 + 1, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D4 VALUES(?,?,?);", (i*2 + 2, start_pos + step*i, wbitlen))

    ################################################################################
    # Таблица со словами TR2NEW2012_D_D5

    # Table WT_TR2NEW2012_D_D5
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    # Каждое 16-ти разрядное слово разбивается на 2 8-разрядных части. Части меняем местами
    numword = 50  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 96  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);", (i*2 + 1, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);", (i*2 + 2, start_pos + step*i, wbitlen))

    numword = 50  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 50*2  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 4992  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i, wbitlen))

    numword = 44  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 100*2  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 9888  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i, wbitlen))

    numword = 2  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 144*2  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 14208  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i, wbitlen))

    numword = 2  # количество слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 146*2  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 14496  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 16//2  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numword):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i + 8, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D5 VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i, wbitlen))

    ################################################################################
    # Таблица со словами TR2NEW2012_D_A
    # Table WT_TR2NEW2012_D_A
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    numgroup = 50  # количество групп слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 0  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 112  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 8  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numgroup):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_A VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_A VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i + 8, wbitlen))

    numgroup = 50  # количество групп слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 100  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 5008  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 8  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numgroup):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_A VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_A VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i + 8, wbitlen))

    numgroup = 50  # количество групп слов коммутатора в вышестоящем коммутаторе PARENT
    countword = 200  # ссылка на предыдущую запись
    step = 96  # смещение между словами коммутатора в вышестоящем коммутаторе PARENT
    start_pos = 9904  # позиция первого слова коммутатора в вышестоящем коммутаторе PARENT
    wbitlen = 8  # длина вырезаемого фрагмента в вышестоящем коммутаторе PARENT
    for i in range(numgroup):
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_A VALUES(?,?,?);",
                        (i*2 + 1 + countword, start_pos + step*i, wbitlen))
        conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_A VALUES(?,?,?);",
                        (i*2 + 2 + countword, start_pos + step*i + 8, wbitlen))

    ################################################################################
    # Таблица со словами TR2NEW2012_D_D4_mode
    # Table WT_TR2NEW2012_D_D4_mode
    # WORDID INTEGER PRIMARY KEY
    # BITPOSINPARENT INTEGER
    # WBITLEN INTEGER
    conn_bd.execute("INSERT INTO WT_TR2NEW2012_D_D4_mode VALUES(?,?,?);", (1, 224, 16))

    conn_bd.commit()
    conn_bd.close()
    print("Populating successfully")


def main():
    parser = argparse.ArgumentParser(description="DB creator converter")
    parser.add_argument('-c', '--create', help="Instruct to create tables", action="store_true", default='-c')
    parser.add_argument('-p', '--populate', help="Instruct to populate table of DB", action="store_true", default='-p')
    parser.add_argument('-o', '--outbase', help="Output database name", default="TLMdb.sqb")
    
    args = parser.parse_args() 
    if args.create:
        print("Creating tables in ", args.outbase, "...")
        create_tables(args.outbase)
    if args.populate:
        print("Populating tables")
        populate_bdtlm(args.outbase)
    # while True:
    #     time.sleep(5) 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting on SIGINT")
    except BaseException as e:
        print("Exiting on exception: "+str(e))
    else:
        print("Exiting on connection loss")  