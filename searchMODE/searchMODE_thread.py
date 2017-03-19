from PyQt5.QtCore import QThread, pyqtSignal
from subprocess import Popen, PIPE, SubprocessError
import os
from time import sleep

class SMODE_thread(QThread):
    s_prbar_SMode = pyqtSignal(int)
    s_error = pyqtSignal(str)
    s_findMODE = pyqtSignal(int)
    
    def __init__(self, fnames, numOrder, timeInterval, sampleFreq, minNumModes, maxNumModes, filesModes):
        super().__init__()
        self.stop_flag = False
        self.pause = False
        self.fnames = fnames
        self.numOrder = numOrder
        self.timeInterval = timeInterval
        self.sampleFreq = sampleFreq
        self.minNumModes = minNumModes
        self.maxNumModes = maxNumModes
        self.filesModes = filesModes
        filesList = os.listdir(self.fnames[0])
        if len(filesList) < 1:
            raise BaseException('In the catalog a little of files.')
    
    def run(self):
        files_names = os.listdir(self.fnames[0]) # Список имен файлов
        progress = float(0)
        stepprogress = 1/len(files_names)
        numFilesMode = 0
        for fileName in files_names: 
            rezult = ''
            numModInChan = ''
            curFileName = self.fnames[0]+'/'+fileName# Формирование полного пути
            try:
                child_proc = Popen(['./searcher_mode.exe', '-i', curFileName, '-t', str(self.timeInterval), 
                                    '-f', str(self.sampleFreq), '-l', str(self.minNumModes), 
                                    '-b', str(self.maxNumModes), '-o', str(self.numOrder)], 
                                   stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=8)
                [out_bytes, err_bytes] = child_proc.communicate(timeout=60)
            except SubprocessError as err:
                print(err)
                self.s_error.emit('Ошибка обработки файла:\n' + err)
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
                numFilesMode += 1
                for line in out_txt:
                    line = line.split(' ')
                    if line[0].find('Number') >= 0 and len(line) > 1:
                        numModInChan = line[3]
                        break
                newList = [curFileName, numModInChan]
                self.filesModes.append(newList)
                self.s_findMODE.emit(int(numFilesMode))
            progress += stepprogress
            self.s_prbar_SMode.emit(int(progress*100))
            if self.stop_flag:
                break
            while self.pause:
                sleep(1)
            

