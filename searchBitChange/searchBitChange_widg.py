import os
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QGroupBox, QLabel, QSizePolicy
from PyQt5.QtWidgets import QSpinBox, QFileDialog, QProgressBar
from PyQt5.QtWidgets import QMessageBox, QTextEdit
from searchBitChange.searchBitChange_thread import SBitChange_thread


class SBitChange_MainWidg(QWidget):
    def __init__(self, path, numOrder, numberBit, minNumChange, maxNumChange):
        super().__init__()
        self.init_var()
        self.init_ui()
        self.ComLine_init(path, numOrder, numberBit, minNumChange, maxNumChange)
    
    def init_var(self):
        self.fnames = list()
        self.numOrder = None
        self.numberBit = None
        self.minNumChange = None
        self.maxNumChange = None
        self.searcher = None
        self.rezultNum = 0
        self.ordersList = list()
        
    def init_ui(self):
        # Описание модуля
        self.lbl_descr = self.lbl_descr_init()
        # Кнопка Старт
        self.btn_start = self.btn_start_init()
        # Настройка параметров поиска
        self.gbox_param = QGroupBox('Настройка параметров поиска')
        self.gbox_path = QGroupBox('Выберите каталог с демультиплексированными файлами...')
        self.btn_path = self.btn_path_init()
        self.lbl_path = QLabel('')
        self.lbl_numord = QLabel('Количество разрядов телеметрических каналов')
        self.spin_numord = self.spin_numord_init()
        self.lbl_numberBit = QLabel('Количество последовательных разрядов')
        self.spin_numberBit = self.spin_numberBit_init()
        self.lbl_minNumChange = QLabel('Минимальное количество изменений разряда в канале')
        self.spin_minNumChange = self.spin_minNumChange_init()
        self.lbl_maxNumChange = QLabel('Максимальное количество изменений разряда в канале')
        self.spin_maxNumChange = self.spin_maxNumChange_init()
        # Прогресс БАР
        self.prbar_SBitChange = QProgressBar()
        self.prbar_SBitChange.setStatusTip('Прогресс поиска')
        # Textedit с результатами
        self.txtedt_rez = self.txtedt_rez_init()
        self.lbl_rez = QLabel('Найденные разряды:')
        # Управление макетом
        self.cur_layout = self.layout_init()
        self.setLayout(self.cur_layout)
        
    def ComLine_init(self, path, numOrder, numberBit, minNumChange, maxNumChange):
        # Донастройка параметров командной строки
        if (path == None or numberBit == None or numOrder == None or 
            minNumChange == None or maxNumChange == None):
            return
        self.numberBit = numberBit
        self.spin_numberBit.setValue(numberBit)
        self.spin_numord.setValue(numOrder)
        self.numOrder = numOrder
        self.lbl_path.setText(path)
        self.fnames.append(path)
        self.spin_minNumChange.setValue(minNumChange)
        self.minNumChange = minNumChange
        self.spin_maxNumChange.setValue(maxNumChange)
        self.maxNumChange = maxNumChange
        # запуск задачи
        self.start_SBitChange_thread()
        
    def lbl_descr_init(self):
        descr = '<div align="center">Программа поиска разрядов с заданным количеством изменений.</div>'
        self.lbl_descr = QLabel(descr)
        self.lbl_descr.setWordWrap(True)
        self.lbl_descr.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        return self.lbl_descr
        
    def btn_start_init(self):
        self.btn_start = QPushButton('Старт')
        self.btn_start.resize(self.btn_start.sizeHint())  # Рекомедуемый размер кнопки
        self.btn_start.setStatusTip('Запуск и остановка поиска')
        self.btn_start.setDisabled(True)
        self.btn_start.clicked.connect(self.start_SBitChange_thread)
        return self.btn_start
    
    def txtedt_rez_init(self):
        self.txtedt_rez = QTextEdit()
        self.txtedt_rez.setReadOnly(True)
        self.txtedt_rez.setStatusTip('Список найденных разрядов')
        self.txtedt_rez.setMinimumSize(200, 300)
        return self.txtedt_rez
    
    def btn_path_init(self):
        self.btn_path = QPushButton('Выбрать...')
        self.btn_path.resize(self.btn_path.sizeHint())
        self.btn_path.clicked.connect(self.showDlg_path)
        self.btn_path.setStatusTip('Выбор каталога ...')
        return self.btn_path
    
    def spin_numord_init(self):
        self.spin_numord = QSpinBox(self)
        self.spin_numord.setMinimumWidth(40)
        self.spin_numord.setMaximumWidth(60)
        self.spin_numord.setValue(16)
        self.spin_numord.setMaximum(64)
        self.spin_numord.setMinimum(8)
        self.spin_numord.setSingleStep(8)
        self.spin_numord.valueChanged.connect(self.spin_numordCHng)
        self.spin_numord.editingFinished.connect(self.get_Numord)
        self.spin_numord.setStatusTip('Введите количество разрядов телеметрических каналов')
        return self.spin_numord

    def spin_numordCHng(self):
        if self.spin_numord.value() < 8:
            self.spin_numord.setValue(8)
        elif self.spin_numord.value() > 64:
            self.spin_numord.setValue(64)

    def spin_numberBit_init(self):
        self.spin_numberBit = QSpinBox(self)
        self.spin_numberBit.setMinimumWidth(40)
        self.spin_numberBit.setMaximumWidth(60)
        self.spin_numberBit.setMaximum(64)
        self.spin_numberBit.setMinimum(1)
        self.spin_numberBit.setValue(3)
        self.spin_numberBit.editingFinished.connect(self.spin_numberBitCHng)
        self.spin_numberBit.setStatusTip('Введите количество расположенных последовательно разрядов')
        return self.spin_numberBit

    def spin_numberBitCHng(self):
        if self.spin_numberBit.value() < 1:
            self.spin_numberBit.setValue(1)
        elif self.spin_numberBit.value() > 64:
            self.spin_numberBit.setValue(64)
    
    def spin_minNumChange_init(self):
        self.spin_minNumChange = QSpinBox(self)
        self.spin_minNumChange.setMinimumWidth(60)
        self.spin_minNumChange.setMaximumWidth(80)
        self.spin_minNumChange.setValue(1)
        self.spin_minNumChange.setMaximum(65536)
        self.spin_minNumChange.setMinimum(1)
        self.spin_minNumChange.valueChanged.connect(self.spin_minNumChangeCHng)
        self.spin_minNumChange.editingFinished.connect(self.spin_minNumChangeCHng)
        self.spin_minNumChange.setStatusTip('Введите минимальное количество изменений разрядов')
        return self.spin_minNumChange
    
    def spin_minNumChangeCHng(self):
        if self.spin_minNumChange.value() < 1:
            self.spin_minNumChange.setValue(1)
        elif self.spin_minNumChange.value() > 65536:
            self.spin_minNumChange.setValue(65536)
        if self.spin_minNumChange.value() >= self.spin_maxNumChange.value():
            self.spin_minNumChange.setValue(self.spin_maxNumChange.value())
            
    def spin_maxNumChange_init(self):
        self.spin_maxNumChange = QSpinBox(self)
        self.spin_maxNumChange.setMinimumWidth(60)
        self.spin_maxNumChange.setMaximumWidth(80)
        self.spin_maxNumChange.setValue(1)
        self.spin_maxNumChange.setMaximum(65536)
        self.spin_maxNumChange.setMinimum(1)
        self.spin_maxNumChange.setSingleStep(1)
        self.spin_maxNumChange.valueChanged.connect(self.spin_maxNumChangeCHng)
        self.spin_maxNumChange.editingFinished.connect(self.spin_maxNumChangeCHng)
        self.spin_maxNumChange.setStatusTip('Введите максимальное количество изменений разрядов')
        return self.spin_maxNumChange
    
    def spin_maxNumChangeCHng(self):
        if self.spin_maxNumChange.value() < 1:
            self.spin_maxNumChange.setValue(1)
        elif self.spin_maxNumChange.value() > 65536:
            self.spin_maxNumChange.setValue(65536)
        if self.spin_maxNumChange.value() <= self.spin_minNumChange.value():
            self.spin_maxNumChange.setValue(self.spin_minNumChange.value())
            
    def showDlg_path(self):
        dir_path = '..'
        dlg_files = QFileDialog()
        dlg_files.setFileMode(QFileDialog.Directory)
        dlg_files.setLabelText(QFileDialog.LookIn, 'Открыть каталог с демультиплексированными файлами ...')
        dlg_files.setAcceptMode(QFileDialog.AcceptOpen)
        dlg_files.setDirectory(dir_path)
        dlg_files.setOption(QFileDialog.ShowDirsOnly)
        if dlg_files.exec_():
            self.fnames = dlg_files.selectedFiles()
            self.lbl_path.setText(self.fnames[0])
            self.btn_start.setEnabled(True)
            
    def showDlgErr(self, err):
        dlg_err = QMessageBox()
        dlg_err.setIcon(QMessageBox.Warning)
        dlg_err.setWindowTitle('Ошибка')
        dlg_err.setText(err)
        dlg_err.setStandardButtons(QMessageBox.Ok)
        dlg_err.buttonClicked.connect(self.showDlgErr_ok)
        self.searcher.pause = True
        dlg_err.exec_()
        
    def showDlgErr_ok(self, i):
        self.searcher.pause = False
                
    def start_SBitChange_thread(self):
        if self.searcher != None:
            self.searcher.disconnect()
            self.searcher = None
        self.spin_numordCHng()
        self.numOrder = self.get_Numord()
        self.numberBit = self.spin_numberBit.value()
        self.minNumChange = self.spin_minNumChange.value()
        self.maxNumChange = self.spin_maxNumChange.value()
        self.ordersList = list()
        try:
            self.searcher = SBitChange_thread(self.fnames, self.numOrder, self.numberBit,
                                              self.minNumChange, self.maxNumChange, self.ordersList)
            self.searcher.s_prbar_SBitChange.connect(self.prbar_SBitChange.setValue)
            self.searcher.started.connect(self.started_SBitChange_thread)
            self.searcher.s_error[str].connect(self.showDlgErr)
            self.searcher.finished.connect(self.finished_SBitChange_thread)
            self.searcher.s_findOrder[int].connect(self.rezult_update)
        except BaseException as err:
            print(err)
            self.showDlgErr(err)
            self.stop_SBitChange_thread()
        self.spin_numord.setDisabled(True)
        self.spin_numberBit.setDisabled(True)
        self.spin_minNumChange.setDisabled(True)
        self.spin_maxNumChange.setDisabled(True)
        self.btn_start.setDisabled(True)
        self.txtedt_rez.clear()
        self.searcher.start()
        #self.searcher.run()
        
    def get_Numord(self):
        if (self.spin_numord.value() != 8 and self.spin_numord.value() != 16 and 
            self.spin_numord.value() != 32 and self.spin_numord.value() != 64):
            if (self.spin_numord.value() < 8):
                self.spin_numord.setValue(8)
            if (self.spin_numord.value() > 8 and self.spin_numord.value() < 16):
                if self.spin_numord.value() < 12:
                    self.spin_numord.setValue(8)
                else:
                    self.spin_numord.setValue(12)
            elif (self.spin_numord.value() > 16 and self.spin_numord.value() < 32):
                if self.spin_numord.value() < 24:
                    self.spin_numord.setValue(16)
                else:
                    self.spin_numord.setValue(32)
            else:
                if self.spin_numord.value() < 48:
                    self.spin_numord.setValue(32)
                else:
                    self.spin_numord.setValue(64)
        return self.spin_numord.value()
                
    def rezult_update(self, i):
        if len(self.ordersList) < 1:
            return
        if len(self.ordersList) > self.rezultNum:
            self.rezultNum += 1
            stroka = str(self.rezultNum) + ': File ' + self.ordersList[self.rezultNum - 1][0]
            stroka += ', position: ' + self.ordersList[self.rezultNum - 1][1]
            stroka += ', length: ' + self.ordersList[self.rezultNum - 1][2]
            self.txtedt_rez.append(stroka)
            print('Orders: ' + stroka)
        else:
            return
        
    def stop_SBitChange_thread(self):
        self.btn_start.setDisabled(True)
        self.searcher.stop_flag =True
        
    def started_SBitChange_thread(self):
        self.btn_start.setText('Стоп')
        self.btn_start.disconnect()
        self.btn_start.clicked.connect(self.stop_SBitChange_thread)
        self.btn_start.setEnabled(True)
        
    def finished_SBitChange_thread(self):
        self.btn_start.setText('Старт')
        self.btn_start.disconnect()
        self.btn_start.clicked.connect(self.start_SBitChange_thread)
        self.btn_start.setEnabled(True)
        self.spin_numord.setEnabled(True)
        self.spin_numberBit.setEnabled(True)
        self.spin_minNumChange.setEnabled(True)
        self.spin_maxNumChange.setEnabled(True)
        self.prbar_SBitChange.reset()
        self.txtedt_rez.append('Всего найдено: ' + str(len(self.ordersList)) + ' последовательностей разрядов.')
        print('Всего найдено: ' + str(len(self.ordersList)) + ' последовательностей разрядов.')
        self.txtedt_rez.append('Подверглось оценке: ' + str(len(os.listdir(self.fnames[0]))) + ' файлов.')
        print('Подверглось оценке: ' + str(len(os.listdir(self.fnames[0]))) + ' файлов.')
        if self.searcher != None:
            self.searcher.disconnect()
            self.searcher = None
        
    def layout_init(self):
        descr_layout = QHBoxLayout()
        descr_layout.addWidget(self.lbl_descr)
        # Группа настройки параметров поиска
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.btn_path)
        path_layout.addWidget(self.lbl_path)
        path_layout.addStretch(1)
        self.gbox_path.setLayout(path_layout)
        param_layout = QVBoxLayout()
        param_layout.addWidget(self.gbox_path)
        param_layout.addWidget(self.lbl_numberBit)
        param_layout.addWidget(self.spin_numberBit)
        param_layout.addWidget(self.lbl_minNumChange)
        param_layout.addWidget(self.spin_minNumChange)
        param_layout.addWidget(self.lbl_maxNumChange)
        param_layout.addWidget(self.spin_maxNumChange)
        param_layout.addWidget(self.lbl_numord)
        param_layout.addWidget(self.spin_numord)
        self.gbox_param.setLayout(param_layout)
        # Последняя строка
        hlayout_lower = QHBoxLayout()
        hlayout_lower.addWidget(self.prbar_SBitChange)
        hlayout_lower.addWidget(self.btn_start)
        # Левый layout
        vbox_left = QVBoxLayout()
        vbox_left.addLayout(descr_layout)
        vbox_left.addWidget(self.gbox_param)
        vbox_left.addStretch(1)
        vbox_left.addLayout(hlayout_lower)
        # Правый layout
        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.lbl_rez)
        vbox_right.addWidget(self.txtedt_rez)
        # Итоговый layout
        hbox_common = QHBoxLayout()
        hbox_common.addLayout(vbox_left)
        hbox_common.addLayout(vbox_right)
        return hbox_common
        