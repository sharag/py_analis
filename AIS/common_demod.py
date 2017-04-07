#!/usr/bin/python3.5
import sys
import glob
import argparse
import os
from subprocess import Popen, PIPE, SubprocessError


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    parser.add_argument('-r', '--recursive', nargs='?', help='Search recursive in input directory: -r', default=False)
    parser.add_argument('-d', '--demodpath', nargs='+', help='Path to the demod file: -d <path>')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.recursive is None:
        namespace.recursive = True
    inpath = namespace.inpath[0]
    if len(namespace.inpath) > 1:
        for i in range(1, len(namespace.inpath)):
            inpath += ' ' + namespace.inpath[i]
    namespace.inpath = inpath
    del inpath
    demodpath = namespace.demodpath[0]
    if len(namespace.demodpath) > 1:
        for i in range(1, len(namespace.demodpath)):
            demodpath += ' ' + namespace.demodpath[i]
    namespace.demodpath = demodpath
    del demodpath
    if namespace.recursive:
        filesList = glob.glob(namespace.inpath + '**//*.iq', recursive=True)
    else:
        filesList = glob.glob(namespace.inpath + '*.iq', recursive=False)
    if len(filesList) < 1:
        raise BaseException('In the catalog a little of files.')
    filesList.sort()
    numfile = 0
    fid_out = open(namespace.inpath + 'rezult.txt', 'w')
    for fileName in filesList:
        numfile += 1
        try:
            child_proc = Popen([namespace.demodpath, '-v', '-m', '8', '-o', '0.48', '-d', '0.02', '-F', '2400000',
                                '-f', fileName, '162050', '161975', '162025'], stdin=PIPE, stdout=PIPE, stderr=PIPE,
                               shell=False)
            [out_bytes, err_bytes] = child_proc.communicate(timeout=3600)
        except SubprocessError as err:
            print(err)
        out_txt = out_bytes.decode('cp1251')
        text = '\r\nFile number: ' + str(numfile) + '/' + str(len(filesList)) + '\r\n'
        fid_out.write(text)
        print(text)
        text = 'File name: ' + fileName + '\r\n'
        fid_out.write(text)
        print(text)
        del text
        fid_out.write(out_txt)
        print(out_txt)
        fid_out.flush()
    fid_out.close()
