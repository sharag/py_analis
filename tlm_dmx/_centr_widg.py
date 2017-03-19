#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, \
    QLabel, QComboBox, QGroupBox, QProgressBar, QCheckBox
from _db_query import DbQuery
from _thread_dmx import Thread_dmx


class MainWidg(QWidget):
    def __init__(self, main_win_ex):
        super().__init__()
        self.main_win_ex = main_win_ex
        self.init_var()
        self.init_ui()

    def init_var(self):
        self.sourse = None
        self.fname_db = ''
        self.object = ''
        self.type = ''
        self.subtype = ''
        self.country = ''
        self.rlname = ''
        self.main_fr_prm = []
        self.channels = []
        self.slctd_chan = []
        self.fname_gts = ''
        self.dmx = None

    def init_ui(self):
        # Кнопка Старт
        self.start_btn = self.start_btn_init()
        # Кнопка выхода
        self.quit_btn = self.quit_btn_init()
        ###############################################################################################################
        # Кнопка выбора файла базы данных
        self.select_db_btn = self.select_db_btn_init()
        self.lbl_db_path = QLabel(self)
        self.lbl_db_path.setStatusTip('Путь к файлу базы данных')
        ###############################################################################################################
        # Кнопка выбора файла ГТС
        self.select_GTS_btn = self.select_GTS_btn_init()
        self.lbl_GTS_path = QLabel(self)
        self.lbl_GTS_path.setStatusTip('Путь к файлу ГТС')
        self.chk_revers = QCheckBox('Реверс бит в байте')
        self.chk_revers.setStatusTip('Если файл ГТС уже был обработан, то реверс был произведен')
        self.chk_revers.setChecked(True)
        self.chk_revers.adjustSize()
        ###############################################################################################################
        # Выбор исследуемого источника
        self.gbox_object = QGroupBox('Выбор исследуемого источника', self)
        self.gbox_object.setStatusTip('Последовательно выберите каждый из критериев классификации источников')
        self.lbl_object = QLabel(self)
        self.lbl_type = QLabel(self)
        self.lbl_subtype = QLabel(self)
        self.lbl_country = QLabel(self)
        self.combo_obj = QComboBox(self)
        self.combo_obj.setMinimumWidth(80)
        self.combo_obj.setStatusTip('Выберите объект')
        self.combo_type = QComboBox(self)
        self.combo_type.setMinimumWidth(50)
        self.combo_type.setStatusTip('Выберите тип источника')
        self.combo_subtype = QComboBox(self)
        self.combo_subtype.setMinimumWidth(80)
        self.combo_subtype.setStatusTip('Выберите подтип источника')
        self.combo_country = QComboBox(self)
        self.combo_country.setMinimumWidth(150)
        self.combo_country.setStatusTip('Выберите страну, которой принадлежит исследуемый объект')
        ###############################################################################################################
        # Выбор радиолинии
        self.gbox_rl = QGroupBox('Выбор радиолинии ', self)
        self.gbox_rl.setStatusTip('Выберите одну из радиолиний, принадлежащих указанному источнику')
        self.lbl_rlname = QLabel(self)
        self.combo_rlname = QComboBox(self)
        self.combo_rlname.setMinimumWidth(250)
        ###############################################################################################################
        # Отображение параметров основного коммутатора
        self.gbox_fr_prm = QGroupBox('Характеристики основного коммутатора', self)
        self.gbox_fr_prm.setStatusTip('Характеристики основного коммутатора')
        self.lbl_fr_name = QLabel(self)
        self.lbl_fr_len = QLabel(self)
        self.lbl_fr_wlen = QLabel(self)
        self.lbl_fr_freq = QLabel(self)
        ###############################################################################################################
        # Выбор коммутатора для демультиплексирования
        self.gbox_sel_chan = QGroupBox('Выбор демультиплексируемого канала', self)
        self.gbox_sel_chan.setStatusTip('Сначала выберите тип, а затем имя демультиплексируемого канала')
        self.lbl_type_chan = QLabel(self)
        self.lbl_type_chan.setMinimumWidth(100)
        self.lbl_name_chan = QLabel(self)
        self.lbl_type_chan.setMinimumWidth(150)
        self.combo_chtype = QComboBox(self)
        self.combo_chtype.setMinimumWidth(100)
        self.combo_chtype.setStatusTip('Выберите тип канала')
        self.combo_chname = QComboBox(self)
        self.combo_chname.setMinimumWidth(200)
        self.combo_chname.setStatusTip('Выберите имя канала')
        ################################################################################################################
        # Отображение параметров выбранного для демультиплексирования канала
        self.gbox_chan_prm = QGroupBox('Характеристики демультиплексируемого канала', self)
        self.gbox_chan_prm.setStatusTip('Характеристики демультиплексируемого канала')
        self.lbl_chan_frlen = QLabel(self)
        self.lbl_chan_wlen = QLabel(self)
        # Прогресс БАР
        self.progrbar_dmx = QProgressBar()
        self.progrbar_dmx.setStatusTip('Прогресс выполнения декоммутации')
        ############################
        self.combo_obj_rm()
        # Управление макетом
        self.cur_layout = self.layout_init()
        self.setLayout(self.cur_layout)

    def start_btn_init(self):
        self.start_btn = QPushButton('Старт')  # QPushButton(string_text, QWidget parent = None)
        self.start_btn.resize(self.start_btn.sizeHint())  # Рекомедуемый размер кнопки
        self.start_btn.setStatusTip('Запуск и остановка декоммутациии')
        self.start_btn.setDisabled(True)
        self.start_btn.clicked.connect(self.start_dmx_thread)
        return self.start_btn

    def quit_btn_init(self):
        self.quit_btn = QPushButton('Выход')
        self.quit_btn.clicked.connect(self.main_win_ex.exit_msg)
        self.quit_btn.resize(self.quit_btn.sizeHint())  # Рекомедуемый размер кнопки
        self.quit_btn.setStatusTip('Выход из приложения')
        return self.quit_btn

    def select_db_btn_init(self):
        self.select_db_btn = QPushButton('Выбор файла БД...')
        self.select_db_btn.setStatusTip('Выбор файла БД...')
        self.select_db_btn.resize(self.select_db_btn.sizeHint())  # Рекомедуемый размер кнопки
        self.select_db_btn.clicked.connect(self.dialog_select_db)
        return self.select_db_btn
    
    def select_GTS_btn_init(self):
        self.select_GTS_btn = QPushButton('Выбор файла ГТС...')
        self.select_GTS_btn.setStatusTip('Выбор файла ГТС...')
        self.select_GTS_btn.resize(self.select_GTS_btn.sizeHint())
        self.select_GTS_btn.setDisabled(True)
        self.select_GTS_btn.clicked.connect(self.dialog_select_gts)
        return self.select_GTS_btn
    
    def dialog_select_gts(self):
        self.fname_gts = QFileDialog.getOpenFileName(self, 'Выберите файл GTS', './', '*.bit')
        if len(self.fname_gts[0]) > 0:
            if self.dmx != None:
                self.dmx.disconnect()
                self.dmx = None
            try:
                self.dmx = Thread_dmx(self.fname_gts[0], self.slctd_chan, self.chk_revers.isChecked())
            except BaseException as err:
                self.main_win_ex.err_msg(err)
                return
            self.lbl_GTS_path.setText(self.fname_gts[0])
            self.lbl_GTS_path.adjustSize()
            self.start_btn.setEnabled(True)
            self.dmx.sprogress_br.connect(self.progrbar_dmx.setValue)
            self.dmx.started.connect(self.dmx_on_started)
            self.dmx.finished.connect(self.dmx_on_finished)
            self.dmx.s_eof.connect(self.main_win_ex.exit_msg)
            self.dmx.s_error.connect(self.main_win_ex.err_msg)

    def dialog_select_db(self):
        self.fname_db = QFileDialog.getOpenFileName(self, 'Выберите файл БД', './', '*.sqb')
        if len(self.fname_db[0]) > 0:
            self.combo_obj_rm()
            self.lbl_db_path.setText(self.fname_db[0])
            self.lbl_db_path.adjustSize()
            try:
                self.sourse = DbQuery(self.fname_db[0], self.main_win_ex)
                combo_init(self.sourse.get_objects(), self.combo_obj)
            except BaseException as err:
                self.main_win_ex.err_msg(err)
            self.combo_obj.activated[str].connect(self.activ_combo_obj)
            self.combo_obj.setEnabled(True)
            
    def start_dmx_thread(self):
        self.combo_obj.setDisabled(True)
        self.combo_type.setDisabled(True)
        self.combo_subtype.setDisabled(True)
        self.combo_country.setDisabled(True)
        self.combo_rlname.setDisabled(True)
        self.combo_chtype.setDisabled(True)
        self.combo_chname.setDisabled(True)
        self.select_GTS_btn.setDisabled(True)
        self.select_db_btn.setDisabled(True)
        self.start_btn.setDisabled(True)
        self.dmx.stop_flag = False
        # Обвязка для ошибок
        self.dmx.start()
        
    def stop_dmx_thread(self):
        self.combo_obj.setEnabled(True)
        self.combo_type.setEnabled(True)
        self.combo_subtype.setEnabled(True)
        self.combo_country.setEnabled(True)
        self.combo_rlname.setEnabled(True)
        self.combo_chtype.setEnabled(True)
        self.combo_chname.setEnabled(True)
        self.select_GTS_btn.setEnabled(True)
        self.select_db_btn.setEnabled(True)
        self.start_btn.setDisabled(True)
        self.dmx.stop_flag = True
        
    def dmx_on_started(self):
        self.start_btn.setText('Стоп')
        self.start_btn.disconnect()
        self.start_btn.clicked.connect(self.stop_dmx_thread)
        self.start_btn.setEnabled(True)
        
    def dmx_on_finished(self):
        self.combo_obj.setEnabled(True)
        self.combo_type.setEnabled(True)
        self.combo_subtype.setEnabled(True)
        self.combo_country.setEnabled(True)
        self.combo_rlname.setEnabled(True)
        self.combo_chtype.setEnabled(True)
        self.combo_chname.setEnabled(True)
        self.select_GTS_btn.setEnabled(True)
        self.select_db_btn.setEnabled(True)
        self.progrbar_dmx.reset()
        if self.dmx != None:
            self.dmx.disconnect()
            self.dmx = None
        try:
            self.dmx = Thread_dmx(self.fname_gts[0], self.slctd_chan, self.chk_revers.isChecked())
        except BaseException as err:
            self.main_win_ex.err_msg(err)
            return
        self.dmx.sprogress_br.connect(self.progrbar_dmx.setValue)
        self.dmx.started.connect(self.dmx_on_started)
        self.dmx.finished.connect(self.dmx_on_finished)
        self.dmx.s_eof.connect(self.main_win_ex.exit_msg)
        self.dmx.s_error.connect(self.main_win_ex.err_msg)
        self.start_btn.setText('Cтарт')
        self.start_btn.disconnect()
        self.start_btn.clicked.connect(self.start_dmx_thread)
        self.start_btn.setEnabled(True)
        
#########################################################################################################################################################################

    def activ_combo_obj(self, text):
        self.combo_type_rm()
        if text == '--':
            self.lbl_object.setText('Объект: ')
            self.lbl_object.adjustSize()
            return
        self.lbl_object.setText('Объект: ' + text)
        self.lbl_object.adjustSize()
        self.object = text
        try:
            combo_init(self.sourse.get_types(self.object), self.combo_type)
        except BaseException as err:
            self.main_win_ex.err_msg(err)
        self.combo_type.activated[str].connect(self.active_combo_type)
        self.combo_type.setEnabled(True)

    def active_combo_type(self, text):
        self.combo_subtype_rm()
        if text == '--':
            self.lbl_type.setText('Тип: ')
            self.lbl_type.adjustSize()
            return
        self.lbl_type.setText('Тип: ' + text)
        self.lbl_type.adjustSize()
        self.type = text
        try:
            combo_init(self.sourse.get_subtypes(self.object, self.type), self.combo_subtype)
        except BaseException as err:
            self.main_win_ex.err_msg(err)
        self.combo_subtype.activated[str].connect(self.active_combo_subtype)
        self.combo_subtype.setEnabled(True)

    def active_combo_subtype(self, text):
        self.combo_country_rm()
        if text == '--':
            self.lbl_subtype.setText('Подтип: ')
            self.lbl_subtype.adjustSize()
            return
        self.lbl_subtype.setText('Подтип: ' + text)
        self.lbl_subtype.adjustSize()
        self.subtype = text
        try:
            combo_init(self.sourse.get_country(self.object, self.type, self.subtype), self.combo_country)
        except BaseException as err:
            self.main_win_ex.err_msg(err)
        self.combo_country.activated[str].connect(self.active_combo_country)
        self.combo_country.setEnabled(True)

    def active_combo_country(self, text):
        self.combo_rlname_rm()
        if text == '--':
            self.lbl_country.setText('Страна: ')
            self.lbl_country.adjustSize()
            return
        self.lbl_country.setText('Страна: ' + text)
        self.lbl_country.adjustSize()
        self.country = text
        try:
            combo_init(self.sourse.get_rl(self.object, self.type, self.subtype, self.country), self.combo_rlname)
        except BaseException as err:
            self.main_win_ex.err_msg(err)
        self.combo_rlname.activated[str].connect(self.active_combo_rlname)
        self.combo_rlname.setEnabled(True)

    def active_combo_rlname(self, text):
        self.combo_chtype_rm()
        if text == '--':
            self.lbl_rlname.setText('Тип радиолинии: ')
            self.lbl_rlname.adjustSize()
            return
        self.lbl_rlname.setText('Тип радиолинии: ' + text)
        self.lbl_rlname.adjustSize()
        self.rlname = text
        try:
            self.main_fr_prm = self.sourse.get_main_frame(self.rlname)
        except BaseException as err:
            self.main_win_ex.err_msg(err)
        self.gbox_fr_prm_set()
        self.channels.append([])
        self.channels[0] = self.main_fr_prm
        try:
            self.sourse.get_all_commuts(self.main_fr_prm[0], self.channels)
        except BaseException as err:
            self.main_win_ex.err_msg(err)
        self.combo_chantype_init()
        self.combo_chtype.setEnabled(True)
        self.combo_chtype.activated[str].connect(self.active_combo_chtype)

    def active_combo_chtype(self, text):
        self.combo_chname_rm()
        if text == '--':
            self.lbl_type_chan.setText('Тип канала: ')
            self.lbl_type_chan.adjustSize()
            return
        self.lbl_type_chan.setText('Тип канала: ' + text)
        self.lbl_type_chan.adjustSize()
        self.combo_channame_init(text)
        self.combo_chname.setEnabled(True)
        self.combo_chname.activated[str].connect(self.active_combo_chname)
        
    def active_combo_chname(self, text):
        if self.dmx != None:
            self.dmx.disconnect()
            self.dmx = None
        self.lbl_GTS_path.setText('')
        self.lbl_GTS_path.adjustSize()
        self.start_btn.setDisabled(True)
        if text == '--':
            self.lbl_name_chan.setText('Имя канала: ')
            self.lbl_name_chan.adjustSize()
            self.lbl_chan_frlen.setText('Длина канала в битах: ')
            self.lbl_chan_frlen.adjustSize()
            self.lbl_chan_wlen.setText('Длина слова в битах: ')
            self.lbl_chan_wlen.adjustSize()
            self.select_GTS_btn.setDisabled(True)
            return
        self.lbl_name_chan.setText('Имя канала: ' + text)
        self.lbl_name_chan.adjustSize()
        self.slctd_chan = []
        self.gbox_chan_prm_set(text)
        self.select_GTS_btn.setEnabled(True)
#########################################################################################################################################################################

    def combo_obj_rm(self):
        while self.combo_obj.count() > 0:
            self.combo_obj.removeItem(0)
        self.lbl_object.setText('Объект: ')
        self.lbl_object.adjustSize()
        self.object = ''
        self.combo_obj.addItem('--')
        self.combo_obj.setDisabled(True)
        self.combo_type_rm()

    def combo_type_rm(self):
        while self.combo_type.count() > 0:
            self.combo_type.removeItem(0)
        self.lbl_type.setText('Тип: ')
        self.lbl_type.adjustSize()
        self.type = ''
        self.combo_type.addItem('--')
        self.combo_type.setDisabled(True)
        self.combo_subtype_rm()

    def combo_subtype_rm(self):
        while self.combo_subtype.count() > 0:
            self.combo_subtype.removeItem(0)
        self.lbl_subtype.setText('Подтип: ')
        self.lbl_subtype.adjustSize()
        self.subtype = ''
        self.combo_subtype.addItem('--')
        self.combo_subtype.setDisabled(True)
        self.combo_country_rm()

    def combo_country_rm(self):
        while self.combo_country.count() > 0:
            self.combo_country.removeItem(0)
        self.lbl_country.setText('Страна: ')
        self.lbl_country.adjustSize()
        self.country = ''
        self.combo_country.addItem('--')
        self.combo_country.setDisabled(True)
        self.combo_rlname_rm()

    def combo_rlname_rm(self):
        while self.combo_rlname.count() > 0:
            self.combo_rlname.removeItem(0)
        self.lbl_rlname.setText('Тип радиолинии: ')
        self.lbl_rlname.adjustSize()
        self.rlname = ''
        self.combo_rlname.addItem('--')
        self.combo_rlname.setDisabled(True)
        self.lbl_fr_name.setText('Условное имя коммутатора: ')
        self.lbl_fr_name.adjustSize()
        self.lbl_fr_len.setText('Длина кадра в битах: ')
        self.lbl_fr_len.adjustSize()
        self.lbl_fr_wlen.setText('Длина слова в битах: ')
        self.lbl_fr_wlen.adjustSize()
        self.lbl_fr_freq.setText('Частота следования кадров в кадр/с: ')
        self.lbl_fr_freq.adjustSize()
        self.main_fr_prm = []
        self.combo_chtype_rm()
        
    def combo_chtype_rm(self):
        self.lbl_type_chan.setText('Тип канала: ')
        self.lbl_type_chan.adjustSize()
        while self.combo_chtype.count() > 0:
            self.combo_chtype.removeItem(0)
        self.combo_chtype.addItem('--')
        self.combo_chtype.setDisabled(True)
        self.channels = []
        self.combo_chname_rm()

    def combo_chname_rm(self):
        self.lbl_name_chan.setText('Имя канала: ')
        self.lbl_name_chan.adjustSize()
        while self.combo_chname.count() > 0:
            self.combo_chname.removeItem(0)
        self.combo_chname.addItem('--')
        self.combo_chname.setDisabled(True)
        self.lbl_chan_frlen.setText('Длина канала в битах: ')
        self.lbl_chan_frlen.adjustSize()
        self.lbl_chan_wlen.setText('Длина слова в битах: ')
        self.lbl_chan_wlen.adjustSize()
        self.slctd_chan = []
        self.fname_gts = ''
        if self.dmx != None:
                self.dmx.disconnect()
                self.dmx = None
        self.lbl_GTS_path.setText('')
        self.lbl_GTS_path.adjustSize()
        self.select_GTS_btn.setDisabled(True)
        self.start_btn.setDisabled(True)
#########################################################################################################################################################################
    
    def select_db_btn_click(self):
        self.select_db_btn.click()

    def layout_init(self):
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(self.select_db_btn)
        hbox_1.addWidget(self.lbl_db_path)
        hbox_1.addStretch(1)

        vbox_gb_obj_1 = QVBoxLayout()
        vbox_gb_obj_1.addWidget(self.lbl_object)
        vbox_gb_obj_1.addWidget(self.combo_obj)
        vbox_gb_obj_2 = QVBoxLayout()
        vbox_gb_obj_2.addWidget(self.lbl_type)
        vbox_gb_obj_2.addWidget(self.combo_type)
        vbox_gb_obj_3 = QVBoxLayout()
        vbox_gb_obj_3.addWidget(self.lbl_subtype)
        vbox_gb_obj_3.addWidget(self.combo_subtype)
        vbox_gb_obj_4 = QVBoxLayout()
        vbox_gb_obj_4.addWidget(self.lbl_country)
        vbox_gb_obj_4.addWidget(self.combo_country)
        gbox_obj_layout = QHBoxLayout()
        gbox_obj_layout.addLayout(vbox_gb_obj_1)
        gbox_obj_layout.addLayout(vbox_gb_obj_2)
        gbox_obj_layout.addLayout(vbox_gb_obj_3)
        gbox_obj_layout.addLayout(vbox_gb_obj_4)
        self.gbox_object.setLayout(gbox_obj_layout)
        vbox_gb_rl_1 = QVBoxLayout()
        vbox_gb_rl_1.addWidget(self.lbl_rlname)
        vbox_gb_rl_1.addWidget(self.combo_rlname)
        gbox_rl_layout = QHBoxLayout()
        gbox_rl_layout.addLayout(vbox_gb_rl_1)
        self.gbox_rl.setLayout(gbox_rl_layout)
        vbox_obj_rl = QVBoxLayout()
        vbox_obj_rl.addWidget(self.gbox_object)
        vbox_obj_rl.addWidget(self.gbox_rl)
        vbox_gbox_frame_layout = QVBoxLayout()
        vbox_gbox_frame_layout.addWidget(self.lbl_fr_name)
        vbox_gbox_frame_layout.addWidget(self.lbl_fr_len)
        vbox_gbox_frame_layout.addWidget(self.lbl_fr_wlen)
        vbox_gbox_frame_layout.addWidget(self.lbl_fr_freq)
        self.gbox_fr_prm.setLayout(vbox_gbox_frame_layout)
        hbox_2 = QHBoxLayout()
        hbox_2.addLayout(vbox_obj_rl)
        hbox_2.addWidget(self.gbox_fr_prm)
        hbox_2.addStretch(1)
        
        vbox_type_chan = QVBoxLayout()
        vbox_type_chan.addWidget(self.lbl_type_chan)
        vbox_type_chan.addWidget(self.combo_chtype)
        vbox_name_chan = QVBoxLayout()
        vbox_name_chan.addWidget(self.lbl_name_chan)
        vbox_name_chan.addWidget(self.combo_chname)
        gbox_chan_layout = QHBoxLayout()
        gbox_chan_layout.addLayout(vbox_type_chan)
        gbox_chan_layout.addLayout(vbox_name_chan)
        self.gbox_sel_chan.setLayout(gbox_chan_layout)
        gbox_chan_prm_layout = QVBoxLayout()
        gbox_chan_prm_layout.addWidget(self.lbl_chan_frlen)
        gbox_chan_prm_layout.addWidget(self.lbl_chan_wlen)
        self.gbox_chan_prm.setLayout(gbox_chan_prm_layout)
        hbox_3 = QHBoxLayout()
        hbox_3.addWidget(self.gbox_sel_chan)
        hbox_3.addWidget(self.gbox_chan_prm)
        hbox_3.addStretch(1)
        
        hbox_4 = QHBoxLayout()
        hbox_4.addWidget(self.select_GTS_btn)
        hbox_4.addWidget(self.lbl_GTS_path)
        hbox_4.addStretch(1)
        
        hbox_5 = QHBoxLayout()
        hbox_5.addWidget(self.chk_revers)
        hbox_5.addStretch(1)
        
        hbox_lower = QHBoxLayout()
#         hbox_lower.addStretch(1)
        hbox_lower.addWidget(self.progrbar_dmx)
        hbox_lower.addWidget(self.start_btn)
        hbox_lower.addWidget(self.quit_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)
        vbox.addLayout(hbox_4)
        vbox.addLayout(hbox_5)
        vbox.addStretch(1)
        vbox.addLayout(hbox_lower)
        return vbox

    def gbox_fr_prm_set(self):
        self.lbl_fr_name.setText('Условное имя коммутатора: ' + self.main_fr_prm[1])
        self.lbl_fr_name.adjustSize()
        self.lbl_fr_len.setText('Длина кадра в битах: ' + str(self.main_fr_prm[3]))
        self.lbl_fr_len.adjustSize()
        self.lbl_fr_wlen.setText('Длина слова в битах: ' + str(self.main_fr_prm[4]))
        self.lbl_fr_wlen.adjustSize()
        self.lbl_fr_freq.setText('Частота следования кадров в кадр/с: ' + str(self.main_fr_prm[5]))
        self.lbl_fr_freq.adjustSize()
        
    def gbox_chan_prm_set(self, chname):
        for i in range(len(self.channels)):
            if self.channels[i][1] == chname:
                self.form_slctd_chan_tab(i)
        self.lbl_chan_frlen.setText('Длина канала в битах: ' + str(self.slctd_chan[0][3]))
        self.lbl_chan_frlen.adjustSize()
        self.lbl_chan_wlen.setText('Длина слова в битах: ' + str(self.slctd_chan[0][4]))
        self.lbl_chan_wlen.adjustSize()
        
    def form_slctd_chan_tab(self, number_chan):
        self.slctd_chan.append([])
        self.slctd_chan[len(self.slctd_chan) - 1] = self.channels[number_chan]
        for i in range(len(self.channels)):
            if self.slctd_chan[len(self.slctd_chan) - 1][2] == self.channels[i][0]:
                self.form_slctd_chan_tab(i)

    def combo_chantype_init(self):
        for i in range(len(self.channels)):
            if self.combo_chtype.count() > 0:
                if self.combo_chtype.findText(self.channels[i][6]) >= 0:
                    continue
                else:
                    self.combo_chtype.addItem(self.channels[i][6])
            else:
                self.combo_chtype.addItem(self.channels[i][6])

    def combo_channame_init(self, chantype):
        for i in range(len(self.channels)):
            if self.channels[i][6] == chantype:
                if self.combo_chname.count() > 0:
                    if self.combo_chname.findText(self.channels[i][1]) >= 0:
                        continue
                    else:
                        self.combo_chname.addItem(self.channels[i][1])
                else:
                    self.combo_chname.addItem(self.channels[i][1])

def combo_init(tab_all, combo):
    for i in range(len(tab_all)):
        if combo.count() > 0:
            if combo.findText(tab_all[i]) >= 0:
                continue
            else:
                combo.addItem(tab_all[i])
        else:
            combo.addItem(tab_all[i])
