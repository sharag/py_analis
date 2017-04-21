import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from graphTMP.graphTMP_win import GraphTMPMainWin
# Образец командной строки
# -p "e:\fedorenko_ns\work\telemetry\trident\07.03.98\work_D\param\T2-1d.bit.11.D1" -o 16 -t uint16 -f 100.0


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-p', '--path', nargs='?', help='Path to the file, str')
    parser_.add_argument('-o', '--numOrder', nargs='?', type=int,
                         help='Number of order in MODE channel, uint[8, 16, 32, 64]')
    parser_.add_argument('-t', '--type_data', nargs='?', type=bool,
                         help='Data type: str[int8, uint8, int16, uint16, int 32, uint32, int64, uint64, float(4b), '
                              'double(8b)]')
    parser_.add_argument('-f', '--frequency', nargs='?', type=float,
                         help='Sampling frequency, float[(>0.0)-...]')
    return parser_


def verify_arg(namespace_):
    path = namespace_.path
    numord = namespace_.numOrder
    type_data = namespace_.type_data
    freq = namespace_.frequency
    if path is not None:
        # Проверка на существование и размер файла (> 20 Мб)
        if not os.path.isfile(path):
            print('Error. File not found.')
            return False
        if os.path.getsize(path) > 20971520:
            print('Error. The file is too large.')
            return False
    else:
        return False
    if numord is not None:
        if numord not in [8, 16, 32, 64]:
            print('Error. Invalid number of order: uint[8, 16, 32, 64].')
            return False
    else:
        return False
    if type_data is not None:
        if type_data in ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float', 'double']:
            print('Error. Invalid data type: str[int8, uint8, int16, uint16, int32, uint32, int64, uint64, float(4b), '
                  'double(8b)].')
            return False
    else:
        return False
    if freq is not None:
        if freq <= 0.0:
            print('Error. Invalid sampling frequency: float[(>0.0)-...].')
            return False
    else:
        return False
    return True


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    app = QApplication(sys.argv)
    if verify_arg(namespace):
        ex = GraphTMPMainWin(namespace.path, namespace.numOrder, namespace.type_data, namespace.frequency)
    else:
        ex = GraphTMPMainWin(None, None, None, None)
    sys.exit(app.exec_())
