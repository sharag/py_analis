#!/usr/bin/python3.5
import sys
import glob
import argparse
import os
from subprocess import Popen, PIPE, SubprocessError


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inpath', nargs='+', help='Path to the input file: -i <path>')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    inpath = namespace.inpath[0]
    if len(namespace.inpath) > 1:
        for i in range(1, len(namespace.inpath)):
            inpath += ' ' + namespace.inpath[i]
    namespace.inpath = inpath
    del inpath
    filesList = glob.glob(namespace.inpath, recursive=False)
    print('Path: ' + namespace.inpath)
    if len(filesList) < 1:
        raise BaseException('Infile not exist.')
    fid_in = open(namespace.inpath, 'r')
    fid_out = open(namespace.inpath + '.out', 'w')
    fid_gps = open(namespace.inpath + '.gps', 'w')
    data_out = ''
    data_GPS = ''
    for line in fid_in:
        line = line.split('\t')
        print('line')
        print(line)
        if len(line) >= 1:
            data_out += line[0] + '\n'
        #if len(line) >= 3:
            #data_out.append('Date&Time: ' + line[1] + '\n')
            #data_out.append('Level: ' + line[2] + '\n')
        if len(line) == 4:
            data_GPS += 'GPS: ' + line[3] + '\n'
    print('\ndataout\n')
    print(data_out)
    print('\ndata_gps\n')
    print(data_GPS)
    fid_in.close()
    fid_out.write(data_out)
    fid_gps.write(data_GPS)
    fid_out.close()
    fid_gps.close()
