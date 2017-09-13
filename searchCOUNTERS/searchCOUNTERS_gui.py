import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from searchCOUNTERS.searchCOUNTERS_win import SCOUNTERS_mainwin

# -p "e:\msvs\tlm_new\Debug\withoutD2_D5\" -o 16 -k 200
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', nargs='?', help='Path to the directory with files')
    parser.add_argument('-k', '--coefficient', nargs='?', type=int, help='The ratio of the number of increments, int[1-10000]')
    parser.add_argument('-o', '--order', nargs='?', type=int, help='Number of bit in channel, int[3-64]')
    return parser

def verifyArg(path, koef, numord):
    if path != None:
        if not os.path.exists(path):
            path = None
            print('Error. Directory not found.')
            return False
    else:
        return False
    if koef != None:
        if (koef < 1 or koef > 10000):
            print('Error. Coefficient out of range.')
            return False
    else:
        return False
    if numord != None:
        if (numord != 8 and numord != 16 and numord != 32 and numord != 64):
            print('Error. Invalid number of order.')
            return False
    else:
        return False
    return True

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    app = QApplication(sys.argv)
    if verifyArg(namespace.path, namespace.coefficient, namespace.order):
        ex = SCOUNTERS_mainwin(namespace.path, namespace.coefficient, namespace.order)
    else:
        ex = SCOUNTERS_mainwin(None,None,None)
    sys.exit(app.exec_())