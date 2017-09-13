from PyQt5.QtCore import QThread, pyqtSignal
from subprocess import Popen, PIPE, SubprocessError
import os
from time import sleep

class SCOUNTERS_thread(QThread):
    s_prbar_SCounter = pyqtSignal(int)
    s_error = pyqtSignal(str)
    s_findCounters = pyqtSignal(int)
    
    def __init__(self, fnames, numord, koef_delta, filesCounters):
        super().__init__()
        self.stop_flag = False
        self.pause = False
        self.fnames = fnames
        self.numord = numord
        self.koef_delta = koef_delta
        self.filesCounters = filesCounters
        filesList = os.listdir(self.fnames[0])
        if len(filesList) < 1:
            raise BaseException('In the catalog a little of files.')
    
    def run(self):
        files_names = os.listdir(self.fnames[0]) # Список имен файлов
        progress = float(0)
        stepprogress = 1/len(files_names)
        numCounters = 0
        for fileName in files_names: 
            rezult = ''
            stepCnt = ''
            curFileName = self.fnames[0]+'/'+fileName# Формирование полного пути
            try:
                child_proc = Popen(['./searcher counters.exe', '-i', curFileName,
                                     '-k', str(self.koef_delta), '-o', 
                                     str(self.numord)], stdin=PIPE, stdout=PIPE, 
                                   stderr=PIPE, creationflags=8)
                [out_bytes, err_bytes] = child_proc.communicate(timeout=60)
            except SubprocessError as err:
                print(err)
                self.s_error.emit('Ошибка обработки файла:\n'+err)
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
                line = line.split(' ')
                if line[0].find('Status') >= 0 and len(line) > 1:
                    rezult = line[1]
                    break
            if rezult.find('True') >= 0:
                numCounters += 1
                for line in out_txt:
                    line = line.split(' ')
                    if line[0].find('Delta') >= 0 and len(line) > 1:
                        stepCnt = line[1]
                        break
                newList = [curFileName, stepCnt]
                self.filesCounters.append(newList)
                self.s_findCounters.emit(int(numCounters))
            progress += stepprogress
            self.s_prbar_SCounter.emit(int(progress*100))
            if self.stop_flag:
                break
            while self.pause:
                sleep(1)
            

