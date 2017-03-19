import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from searchBitChange.searchBitChange_win import SbitChangeMainWin

# -p "e:\msvs\tlm_new\Debug\T2-1a\" -o 8 -n 3 -l 1 -b 3


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-p', '--path', nargs='?', help='Path to the directory with files, str')
    parser_.add_argument('-o', '--numOrder', nargs='?', type=int,
                         help='Number of order in channel, uint[8, 16, 32, 64]')
    parser_.add_argument('-n', '--numberBit', nargs='?', type=float, help='Number of consecutives bits , uint[1 - 64]')
    parser_.add_argument('-l', '--minNumChange', nargs='?', type=int,
                         help='Minimum number of changes in one order, uint[0 - 65536]')
    parser_.add_argument('-b', '--maxNumChange', nargs='?', type=int,
                         help='Maximum number of changes in one order, uint[0 - 65536]')
    return parser_


def verify_arg(namespace_):
    path = namespace_.path
    numord = namespace_.numOrder
    number_bit = namespace_.numberBit
    min_num_chng = namespace_.minNumChange
    max_num_chng = namespace_.maxNumChange
    if path is not None:
        if not os.path.exists(path):
            print('Error. Directory not found.')
            return False
    else:
        return False
    if number_bit is not None:
        if number_bit < 1 or number_bit > 64:
            print('Error. Invalid number of consecutives bits , uint[1 - 64].')
            return False
    else:
        return False
    if numord is not None:
        if numord != 8 and numord != 16 and numord != 32 and numord != 64:
            print('Error. Invalid number of order: uint[8, 16, 32, 64].')
            return False
    else:
        return False
    if min_num_chng is not None:
        if min_num_chng < 1 or min_num_chng > 65536:
            print('Error. Invalid minimum number of changes in one order, uint[0 - 65536].')
            return False
    else:
        return False
    if max_num_chng is not None:
        if max_num_chng < 1 or max_num_chng > 50:
            print('Error. Invalid maximum number of changes in one order, uint[0 - 65536].')
            return False
    else:
        return False
    if min_num_chng > max_num_chng:
        print('Error. Minimum number of changes in one order should be less or equal than maximum.')
        return False
    return True


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    
    app = QApplication(sys.argv)
    if verify_arg(namespace):
        ex = SbitChangeMainWin(namespace.path, namespace.numOrder, namespace.numberBit, namespace.minNumChange,
                                namespace.maxNumChange)
    else:
        ex = SbitChangeMainWin(None, None, None, None, None)
    sys.exit(app.exec_())
