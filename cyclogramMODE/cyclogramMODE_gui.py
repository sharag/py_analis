import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from cyclogramMODE.cyclogramMODE_win import CyclogrMODEMainWin


# -p "e:\msvs\tlm_new\Debug\T2-1a\" -o 8 -n 3 -l 1 -b 3


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-p', '--path', nargs='?', help='Path to the file, str')
    parser_.add_argument('-o', '--numOrder', nargs='?', type=int,
                         help='Number of order in MODE channel, uint[8, 16, 32, 64]')
    return parser_


def verify_arg(namespace_):
    path = namespace_.path
    numord = namespace_.numOrder
    if path is not None:
        if not os.path.exists(path):
            print('Error. File not found.')
            return False
    else:
        return False
    if numord is not None:
        if numord != 8 and numord != 16 and numord != 32 and numord != 64:
            print('Error. Invalid number of order: uint[8, 16, 32, 64].')
            return False
    else:
        return False
    return True


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    app = QApplication(sys.argv)
    if verify_arg(namespace):
        ex = CyclogrMODEMainWin(namespace.path, namespace.numOrder)
    else:
        ex = CyclogrMODEMainWin(None, None)
    sys.exit(app.exec_())
