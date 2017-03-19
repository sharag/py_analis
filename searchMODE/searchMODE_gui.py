import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from searchMODE.searchMODE_win import SMODE_mainwin

# -p "e:\msvs\tlm_new\Debug\withoutD2_D5\" -o 16 -t 5 -f 100 -l 14 -b 16
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', nargs='?', help='Path to the directory with files, str')
    parser.add_argument('-t', '--timeInterval', nargs='?', type=float, help='Time interval in one mode, float[0.1 - 300.0]')
    parser.add_argument('-o', '--numOrder', nargs='?', type=int, help='Number of bit in channel, int[3-64]')
    parser.add_argument('-f', '--sampleFreq', nargs='?', type=float, help='Sampling frequency in Hz, float')
    parser.add_argument('-l', '--minNumModes', nargs='?', type=int, help='minimum number of modes, uint[1 - 50]')
    parser.add_argument('-b', '--maxNumModes', nargs='?', type=int, help='maximum number of modes, uint[1 - 50]')
    return parser

def verifyArg(namespace):
    path = namespace.path
    timeInt = namespace.timeInterval
    numord = namespace.numOrder
    sampleFreq = namespace.sampleFreq
    minNumModes = namespace.minNumModes
    maxNumModes = namespace.maxNumModes
    if path != None:
        if not os.path.exists(path):
            path = None
            print('Error. Directory not found.')
            return False
    else:
        return False
    if timeInt != None:
        if (timeInt < 0.1 or timeInt > float(300)):
            print('Error. Invalid time interval: float[0.1 - 300.0].')
            return False
    else:
        return False
    if numord != None:
        if (numord != 8 and numord != 16 and numord != 32 and numord != 64):
            print('Error. Invalid number of order: uint[8, 16, 32, 64].')
            return False
    else:
        return False
    if sampleFreq == None:
        return False
    if minNumModes != None:
        if minNumModes < 1 or minNumModes > 50:
            print('Error. Invalid minimum number of modes: uint[1 - 50].')
            return False
    else:
        return False
    if maxNumModes != None:
        if maxNumModes < 1 or maxNumModes > 50:
            print('Error. Invalid maximum number of modes: uint[1 - 50].')
            return False
    else:
        return False
    if minNumModes >= maxNumModes:
        print('Error. Minimum number of modes should be less than maximum number of modes.')
        return False
    return True

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    app = QApplication(sys.argv)
    if verifyArg(namespace):
        ex = SMODE_mainwin(namespace.path, namespace.timeInterval, namespace.numOrder, 
                               namespace.sampleFreq, namespace.minNumModes, namespace.maxNumModes)
    else:
        ex = SMODE_mainwin(None,None,None, None, None, None)
    sys.exit(app.exec_())