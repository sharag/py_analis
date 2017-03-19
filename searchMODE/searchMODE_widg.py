import os
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QGroupBox, QLabel, QSizePolicy, QDoubleSpinBox
from PyQt5.QtWidgets import QSpinBox, QFileDialog, QProgressBar
from PyQt5.QtWidgets import QMessageBox, QTextEdit
#from PyQt5.QtCore import Qt
from searchMODE.searchMODE_thread import SMODE_thread

class SMODE_MainWidg(QWidget):
    def __init__(self, path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes):
        super().__init__()
        self.init_var()
        self.init_ui()
        self.spin_sampleFreq.setValue(100.0)
        self.ComLine_init(path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes)
    
    def init_var(self):
        self.fnames = list()
        self.numOrder = None
        self.timeInterval = None
        self.sampleFreq  = None
        self.minNumModes = None
        self.maxNumModes = None
        self.searcher = None
        self.filesModes = list()
        
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
        self.lbl_timeInt = QLabel('Продолжительность работы в одном режиме')
        self.spin_timeInt = self.spin_timeInt_init()
        self.lbl_timeInt_ = QLabel(' c')
        self.lbl_sampleFreq = QLabel('Частота дискретизации каналов')
        self.spin_sampleFreq = self.spin_sampleFreq_init()
        self.lbl_sampleFreq_ = QLabel(' Гц')
        self.lbl_minNumModes = QLabel('Минимальное количество режимов')
        self.spin_minNumModes = self.spin_minNumModes_init()
        self.lbl_maxNumModes = QLabel('Максимальное количество режимов')
        self.spin_maxNumModes = self.spin_maxNumModes_init()
        # Прогресс БАР
        self.prbar_SMode = QProgressBar()
        self.prbar_SMode.setStatusTip('Прогресс поиска')
        # Textedit с результатами
        self.txtedt_rez = self.txtedt_rez_init()
        self.lbl_rez = QLabel('Найденные файлы:')
        # Управление макетом
        self.cur_layout = self.layout_init()
        self.setLayout(self.cur_layout)
        
    def ComLine_init(self, path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes):
        # Донастройка параметров командной строки
        if (path == None or timeInterval == None or numOrder == None or 
            sampleFreq == None or minNumModes == None or maxNumModes == None):
            return
        self.timeInterval = timeInterval
        self.spin_timeInt.setValue(timeInterval)
        self.spin_numord.setValue(numOrder)
        self.numOrder = numOrder
        self.lbl_path.setText(path)
        self.fnames.append(path)
        self.spin_sampleFreq.setValue(sampleFreq)
        self.sampleFreq  = sampleFreq
        self.spin_minNumModes.setValue(minNumModes)
        self.minNumModes = minNumModes
        self.spin_maxNumModes.setValue(maxNumModes)
        self.maxNumModes = maxNumModes
        # запуск задачи
        self.start_SMODE_thread()
        
    def lbl_descr_init(self):
        descr = '<div align="center">Для поиска канала режимов функционирования бортовой СУ необходимо задать следующие параметры:</div><br>'
        descr += '<div align="left">1. Средняя продолжительность работы в одном режиме, в долях секунд.<br>'
        descr += '2. Частота дискретизации каналов, в герцах.<br>'
        descr += '3-4. Предполагаемое количество режимов функционирования бортовой СУ, ограниченное минимальным и максимальным значениями.<br></div>'
        descr += '<div align="justify">    В случае, если в канале присутствует постоянный на заданном периоде участок, '
        descr += 'будет принято решение, что данный участок соответсвует одному режиму функционирования бортовой СУ. '
        descr += 'Если количество найденных режимов соответвует заданному интервалу, канал будет считаться каналом режимов.</div>'
        self.lbl_descr = QLabel(descr)
        self.lbl_descr.setWordWrap(True)
        self.lbl_descr.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        #self.lbl_descr.setAlignment(Qt.AlignCenter)
        return self.lbl_descr
        
    def btn_start_init(self):
        self.btn_start = QPushButton('Старт')
        self.btn_start.resize(self.btn_start.sizeHint())  # Рекомедуемый размер кнопки
        self.btn_start.setStatusTip('Запуск и остановка поиска')
        self.btn_start.setDisabled(True)
        self.btn_start.clicked.connect(self.start_SMODE_thread)
        return self.btn_start
    
    def txtedt_rez_init(self):
        self.txtedt_rez = QTextEdit()
        self.txtedt_rez.setReadOnly(True)
        self.txtedt_rez.setStatusTip('Список найденных файлов')
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

    def spin_timeInt_init(self):
        self.spin_timeInt = QDoubleSpinBox(self)
        self.spin_timeInt.setMinimumWidth(40)
        self.spin_timeInt.setMaximumWidth(60)
        self.spin_timeInt.setSingleStep(0.1)
        self.spin_timeInt.setMaximum(300.0)
        self.spin_timeInt.setMinimum(0.1)
        self.spin_timeInt.setValue(5.0)
        self.spin_timeInt.editingFinished.connect(self.spin_timeIntCHng)
        self.spin_timeInt.setStatusTip('Введите период в долях секунд')
        return self.spin_timeInt

    def spin_timeIntCHng(self):
        if self.spin_timeInt.value() < 0.1:
            self.spin_timeInt.setValue(0.1)
        elif self.spin_timeInt.value() > 300.0:
            self.spin_timeInt.setValue(300.0)
            
    def spin_sampleFreq_init(self):
        self.spin_sampleFreq = QDoubleSpinBox(self)
        self.spin_sampleFreq.setMinimumWidth(40)
        self.spin_sampleFreq.setMaximumWidth(60)
        self.spin_sampleFreq.setSingleStep(1.0)
        self.spin_sampleFreq.setMaximum(10000000.0)
        self.spin_sampleFreq.setValue(100.0)
        self.spin_sampleFreq.setStatusTip('Введите частоту дискретизации в герцах')
        return self.spin_sampleFreq
    
    def spin_minNumModes_init(self):
        self.spin_minNumModes = QSpinBox(self)
        self.spin_minNumModes.setMinimumWidth(40)
        self.spin_minNumModes.setMaximumWidth(60)
        self.spin_minNumModes.setValue(14)
        self.spin_minNumModes.setMaximum(50)
        self.spin_minNumModes.setMinimum(1)
        self.spin_minNumModes.setSingleStep(1)
        self.spin_minNumModes.editingFinished.connect(self.spin_minNumModesCHng)
        self.spin_minNumModes.setStatusTip('Введите минимальное количество режимов')
        return self.spin_minNumModes
    
    def spin_minNumModesCHng(self):
        if self.spin_minNumModes.value() < 1:
            self.spin_minNumModes.setValue(1)
        elif self.spin_minNumModes.value() > 50:
            self.spin_minNumModes.setValue(50)
        if self.spin_minNumModes.value() >= self.spin_maxNumModes.value():
            self.spin_minNumModes.setValue(self.spin_maxNumModes.value() - 1)
            
    def spin_maxNumModes_init(self):
        self.spin_maxNumModes = QSpinBox(self)
        self.spin_maxNumModes.setMinimumWidth(40)
        self.spin_maxNumModes.setMaximumWidth(60)
        self.spin_maxNumModes.setValue(16)
        self.spin_maxNumModes.setMaximum(50)
        self.spin_maxNumModes.setMinimum(1)
        self.spin_maxNumModes.setSingleStep(1)
        self.spin_maxNumModes.editingFinished.connect(self.spin_maxNumModesCHng)
        self.spin_maxNumModes.setStatusTip('Введите максимальное количество режимов')
        return self.spin_maxNumModes
    
    def spin_maxNumModesCHng(self):
        if self.spin_maxNumModes.value() < 1:
            self.spin_maxNumModes.setValue(1)
        elif self.spin_maxNumModes.value() > 50:
            self.spin_maxNumModes.setValue(50)
        if self.spin_maxNumModes.value() <= self.spin_minNumModes.value():
            self.spin_maxNumModes.setValue(self.spin_minNumModes.value() + 1)
            
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
        #msg.setInformativeText('This is additional information')
        #msg.setDetailedText('The details are as follows:')
        
    def showDlgErr_ok(self, i):
        self.searcher.pause = False
                
    def start_SMODE_thread(self):
        if self.searcher != None:
            self.searcher.disconnect()
            self.searcher = None
        self.spin_numordCHng()
        self.numOrder = self.get_Numord()
        self.timeInterval = self.spin_timeInt.value()
        self.sampleFreq  = self.spin_sampleFreq.value()
        self.minNumModes = self.spin_minNumModes.value()
        self.maxNumModes = self.spin_maxNumModes.value()
        self.filesModes = list()
        try:
            self.searcher = SMODE_thread(self.fnames, self.numOrder, self.timeInterval, 
                                         self.sampleFreq, self.minNumModes, self.maxNumModes, self.filesModes)
            self.searcher.s_prbar_SMode.connect(self.prbar_SMode.setValue)
            self.searcher.started.connect(self.started_SMODE_thread)
            self.searcher.s_error[str].connect(self.showDlgErr)
            self.searcher.finished.connect(self.finished_SMODE_thread)
            self.searcher.s_findMODE[int].connect(self.rezult_update)
        except BaseException as err:
            print(err)
            self.showDlgErr(err)
            self.stop_SMODE_thread()
        self.spin_numord.setDisabled(True)
        self.spin_timeInt.setDisabled(True)
        self.spin_sampleFreq.setDisabled(True)
        self.spin_minNumModes.setDisabled(True)
        self.spin_maxNumModes.setDisabled(True)
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
        if len(self.filesModes) < 1:
            return
        stroka = str(i) + ': ' + self.filesModes[i-1][0] + '. Number of modes: ' + self.filesModes[i-1][1]
        self.txtedt_rez.append(stroka)
        print('Counter:' + stroka)
        
    def stop_SMODE_thread(self):
        self.btn_start.setDisabled(True)
        self.searcher.stop_flag =True
        
    def started_SMODE_thread(self):
        self.btn_start.setText('Стоп')
        self.btn_start.disconnect()
        self.btn_start.clicked.connect(self.stop_SMODE_thread)
        self.btn_start.setEnabled(True)
        
    def finished_SMODE_thread(self):
        self.btn_start.setText('Старт')
        self.btn_start.disconnect()
        self.btn_start.clicked.connect(self.start_SMODE_thread)
        self.btn_start.setEnabled(True)
        self.spin_numord.setEnabled(True)
        self.spin_timeInt.setEnabled(True)
        self.spin_sampleFreq.setEnabled(True)
        self.spin_minNumModes.setEnabled(True)
        self.spin_maxNumModes.setEnabled(True)
        self.prbar_SMode.reset()
        self.txtedt_rez.append('Всего найдено: ' + str(len(self.filesModes)) + ' файлов.')
        print('Всего найдено: ' + str(len(self.filesModes)) + ' файлов.')
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
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.spin_timeInt)
        time_layout.addWidget(self.lbl_timeInt_)
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(self.spin_sampleFreq)
        freq_layout.addWidget(self.lbl_sampleFreq_)
        param_layout = QVBoxLayout()
        param_layout.addWidget(self.gbox_path)
        param_layout.addWidget(self.lbl_timeInt)
        param_layout.addLayout(time_layout)
        param_layout.addWidget(self.lbl_sampleFreq)
        param_layout.addLayout(freq_layout)
        param_layout.addWidget(self.lbl_minNumModes)
        param_layout.addWidget(self.spin_minNumModes)
        param_layout.addWidget(self.lbl_maxNumModes)
        param_layout.addWidget(self.spin_maxNumModes)
        param_layout.addWidget(self.lbl_numord)
        param_layout.addWidget(self.spin_numord)
        self.gbox_param.setLayout(param_layout)
        # Последняя строка
        hlayout_lower = QHBoxLayout()
        hlayout_lower.addWidget(self.prbar_SMode)
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
        