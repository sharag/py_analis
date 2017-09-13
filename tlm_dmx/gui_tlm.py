#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from _main_win import MainWin

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())
