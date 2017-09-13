from PyQt5.QtCore import QThread, pyqtSignal
from dmx import Demuxer
# from fileinput import close

class Thread_dmx(QThread):
    sprogress_br = pyqtSignal(int)
    s_eof = pyqtSignal(str)
    s_error = pyqtSignal(str)
    def __init__(self, fname_gts, slct_channels, rev):
        super().__init__()
        self.stop_flag = False
        self.channels = slct_channels
        self.revers = rev
        self.fname_gts = fname_gts
        self.cur_progr = 0
        try:
            self.dmx = Demuxer(self.channels, 0, self.fname_gts, self.revers)
        except BaseException as err:
            raise BaseException(err)
            exit(0)
    
    def run(self):
        global progr
        progr = 0
        self.sprogress_br.emit(progr)
        with open(self.channels[0][1], 'wb') as self.out_fid:
            self.dmx.get_2frames()
            while True:
                if self.cur_progr != progr:
                    self.sprogress_br.emit(progr)
                    self.cur_progr = progr
                if not self.stop_flag:
                    try:
                        self.out_fid.write(self.dmx.get_bits(64).bytes)
                    except BaseException as err:
                        if err == 'EOF':
                            self.s_eof.emit(err)
                            break
                        else:
                            self.s_error.emit(err)
                            break
                else:
                    break

