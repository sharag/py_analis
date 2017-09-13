from PyQt5.QtCore import QThread, pyqtSignal
from subprocess import Popen, PIPE, SubprocessError
import os
from time import sleep

class SBitChange_thread(QThread):
    s_prbar_SBitChange = pyqtSignal(int)
    s_error = pyqtSignal(str)
    s_findOrder = pyqtSignal(int)
    
    def __init__(self, fnames, numOrder, numberBit, minNumChange, maxNumChange, ordersList):
        super().__init__()
        self.stop_flag = False
        self.pause = False
        self.fnames = fnames
        self.numOrder = numOrder
        self.numberBit = numberBit
        self.minNumChange = minNumChange
        self.maxNumChange = maxNumChange
        self.ordersList = ordersList
        filesList = os.listdir(self.fnames[0])
        if len(filesList) < 1:
            raise BaseException('In the catalog a little of files.')
        
        # -i e:\msvs\tlm_new\Debug\T2-1a\T2-1a.bit.177 -o 8 -n 3 -l 1 -b 3
    
    def run(self):
        files_names = os.listdir(self.fnames[0]) # Список имен файлов
        progress = float(0)
        stepprogress = 1/len(files_names)
        numOrders = 0
        for fileName in files_names: 
            curFileName = self.fnames[0]+'/'+fileName# Формирование полного пути
            try:
                child_proc = Popen(['./searcherChangeBits.exe', '-i', curFileName, '-n', str(self.numberBit), 
                                    '-l', str(self.minNumChange), 
                                    '-b', str(self.maxNumChange), '-o', str(self.numOrder)], 
                                   stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=8)
                [out_bytes, err_bytes] = child_proc.communicate(timeout=60)
            except SubprocessError as err:
                print(err)
                self.s_error.emit('Ошибка обработки файла:\n' + curFileName + ' :' + err)
            out_txt = out_bytes.decode('cp1251')#('utf-8')
            out_txt = out_txt.split('\n')
            err_txt = err_bytes.decode('cp1251')#('utf-8')
            err_txt = err_txt.split('\n')
            if len(err_txt[0]) > 2:
                for line in err_txt:
                    linespl = line.split('\n')
                    if linespl[0].find('Error.') >= 0:
                        self.s_error.emit(line + ' File: ' + curFileName)
                    break
                continue
            for line in out_txt:
                linespl = line.split(' ')
                if linespl[0].find('Status') >= 0 and len(linespl) > 1:
                    rezult = linespl[1]
                    break
            if rezult.find('True') >= 0:
                numOrders += 1
                for line in out_txt:
                    line = line.split(' ')
                    if line[0].find('Sequence') >= 0 and len(line) > 1:
                        curOrder = list()
                        curOrder.append(curFileName)
                        curOrder.append(line[3])
                        curOrder.append(line[5])
                        self.ordersList.append(curOrder)
                        self.s_findOrder.emit(int(numOrders))
            progress += stepprogress
            self.s_prbar_SBitChange.emit(int(progress*100))
            if self.stop_flag:
                break
            while self.pause:
                sleep(1)
            

