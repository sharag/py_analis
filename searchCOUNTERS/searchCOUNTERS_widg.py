import os
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QGroupBox, QLabel, QSizePolicy
from PyQt5.QtWidgets import QSpinBox, QFileDialog, QProgressBar
from PyQt5.QtWidgets import QMessageBox, QTextEdit
from PyQt5.QtCore import Qt
from searchCOUNTERS.searchCOUNTERS_thread import SCOUNTERS_thread

class SCOUNTERS_MainWidg(QWidget):
    def __init__(self, path, koefficient, order):
        super().__init__()
        self.init_var()
        self.init_ui()
        self.initComLine(path, koefficient, order)
    
    def init_var(self):
        self.fnames = list()
        self.numord = None
        self.koef_delta = None
        self.searcher = None
        self.filesCounters = list()
        
    def init_ui(self):
        # Описание модуля
        descr = "Для поиска каналов счетчиков используются статистические"
        descr += "характеристики приращений значений телеметрических каналов. "
        descr += "Предполагается, что в канале, содержащем разряды счетчика, "
        descr += "приращения значений, соответствующие шагу счетчика, "
        descr += "встречаются намного чаще, чем остальные приращения. Если "
        descr += "приращение, встретившееся максимальное количество раз, " 
        descr += "встретилось в <b>Коэффициент отношения количества приращений</b>"
        descr += " чаще, чем любое другое приращение, то телеметрический канал "
        descr += "считается каналом счетчика"
        self.lbl_descr = QLabel(descr)
        self.lbl_descr.setWordWrap(True)
        self.lbl_descr.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.lbl_descr.setAlignment(Qt.AlignCenter)
        # Кнопка Старт
        self.btn_start = self.btn_start_init()
        # Настройка параметров поиска
        self.gbox_param = QGroupBox("Настройка параметров поиска")
        self.gbox_path = QGroupBox("Выберите каталог с демультиплексированными файлами...")
        self.btn_path = self.btn_path_init()
        self.lbl_path = QLabel("")
        self.lbl_numord = QLabel("Количество разрядов телеметрических каналов")
        self.spin_numord = self.spin_numord_init()
        self.lbl_koef = QLabel("Коэффициент отношения количества приращений")
        self.spin_koef = self.spin_koef_init()
        # Прогресс БАР
        self.prbar_SCounter = QProgressBar()
        self.prbar_SCounter.setStatusTip('Прогресс поиска')
        # Textedit с результатами
        self.txtedt_rez = self.txtedt_rez_init()
        self.lbl_rez = QLabel('Найденные файлы:')
        # Управление макетом
        self.cur_layout = self.layout_init()
        self.setLayout(self.cur_layout)
        
    def initComLine(self, path, koefficient, order):
        # Донастройка параметров командной строки
        if koefficient != None:
            self.koef_delta = koefficient
            self.spin_koef.setValue(koefficient)
        else:
            return
        self.spin_numord.setValue(order)
        self.numord = order
        self.lbl_path.setText(path)
        self.fnames.append(path)
        # запуск задачи
        self.start_SCNT_thread()
        
        
    def btn_start_init(self):
        self.btn_start = QPushButton('Старт')
        self.btn_start.resize(self.btn_start.sizeHint())  # Рекомедуемый размер кнопки
        self.btn_start.setStatusTip('Запуск и остановка поиска')
        self.btn_start.setDisabled(True)
        self.btn_start.clicked.connect(self.start_SCNT_thread)
        return self.btn_start
    
    def txtedt_rez_init(self):
        self.txtedt_rez = QTextEdit()
        self.txtedt_rez.setReadOnly(True)
        self.txtedt_rez.setStatusTip('Список найденных файлов')
        self.txtedt_rez.setMinimumSize(200, 300)
        return self.txtedt_rez
    
    def btn_path_init(self):
        self.btn_path = QPushButton("Выбрать...")
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
    
    def spin_koef_init(self):
        self.spin_koef = QSpinBox(self)
        self.spin_koef.setMinimumWidth(40)
        self.spin_koef.setMaximumWidth(60)
        self.spin_koef.setSingleStep(10)
        self.spin_koef.setMaximum(10000)
        self.spin_koef.setMinimum(1)
        self.spin_koef.setValue(500)
        self.spin_koef.editingFinished.connect(self.spin_koefCHng)
        self.spin_koef.setStatusTip('Введите коэффициент отношения приращений')
        return self.spin_koef
                
    def spin_numordCHng(self):
        if self.spin_numord.value() < 8:
            self.spin_numord.setValue(8)
        elif self.spin_numord.value() > 64:
            self.spin_numord.setValue(64)
            
    def spin_koefCHng(self):
        if self.spin_koef.value() < 1:
            self.spin_koef.setValue(1)
        elif self.spin_koef.value() > 10000:
            self.spin_koef.setValue(10000)
            
    def showDlg_path(self):
        dir_path = ".."
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
        #msg.setInformativeText("This is additional information")
        #msg.setDetailedText("The details are as follows:")
        
    def showDlgErr_ok(self, i):
        self.searcher.pause = False
                
    def start_SCNT_thread(self):
        if self.searcher != None:
            self.searcher.disconnect()
            self.searcher = None
        self.spin_numordCHng()
        self.numord = self.get_Numord()
        self.koef_delta = self.spin_koef.value()
        self.filesCounters = list()
        try:
            self.searcher = SCOUNTERS_thread(self.fnames, self.numord, self.koef_delta, self.filesCounters)
            self.searcher.s_prbar_SCounter.connect(self.prbar_SCounter.setValue)
            self.searcher.started.connect(self.started_SCOUNTER_thread)
            self.searcher.s_error[str].connect(self.showDlgErr)
            self.searcher.finished.connect(self.finished_SCOUNTER_thread)
            self.searcher.s_findCounters[int].connect(self.rezult_update)
        except BaseException as err:
            print(err)
            self.showDlgErr(err)
            self.stop_SMODE_thread()
        self.spin_numord.setDisabled(True)
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
        if len(self.filesCounters)<1:
            return
        stroka = str(i) + ': ' + self.filesCounters[i-1][0] + '. Delta: ' + self.filesCounters[i-1][1]
        self.txtedt_rez.append(stroka)
        print('Counter:' + stroka)
        
    def stop_SCOUNTER_thread(self):
        self.btn_start.setDisabled(True)
        self.searcher.stop_flag =True
        
    def started_SCOUNTER_thread(self):
        self.btn_start.setText('Стоп')
        self.btn_start.disconnect()
        self.btn_start.clicked.connect(self.stop_SCOUNTER_thread)
        self.btn_start.setEnabled(True)
        
    def finished_SCOUNTER_thread(self):
        self.btn_start.setText('Старт')
        self.btn_start.disconnect()
        self.btn_start.clicked.connect(self.start_SCNT_thread)
        self.btn_start.setEnabled(True)
        self.spin_numord.setEnabled(True)
        self.prbar_SCounter.reset()
        self.txtedt_rez.append('Всего найдено: ' + str(len(self.filesCounters)) + ' файлов.')
        print('Всего найдено: ' + str(len(self.filesCounters)) + ' файлов.')
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
        param_layout.addWidget(self.lbl_koef)
        param_layout.addWidget(self.spin_koef)
        param_layout.addWidget(self.lbl_numord)
        param_layout.addWidget(self.spin_numord)
        self.gbox_param.setLayout(param_layout)
        # Последняя строка
        hlayout_lower = QHBoxLayout()
        hlayout_lower.addWidget(self.prbar_SCounter)
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
        