#!/usr/bin/python3.5
import sys
import glob
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    parser.add_argument('-r', '--recursive', nargs='?', help='Search recursive in input directory: -r', default=False)
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
    if namespace.recursive:
        filesList = glob.glob(namespace.inpath + '**//*.ais', recursive=True)
    else:
        filesList = glob.glob(namespace.inpath + '*.ais', recursive=False)
    print('Path: ' + namespace.inpath)
    if len(filesList) < 1:
        raise BaseException('Infile not exist.')
    numfile = 0
    fid_out = open(namespace.inpath + 'result.out', 'w')
    fid_gps = open(namespace.inpath + 'result.gps', 'w')
    for fileName in filesList:
        numfile += 1
        fid_in = open(fileName, 'r')

        text = '\nFile number: ' + str(numfile) + '/' + str(len(filesList)) + '\n'
        fid_out.write(text)
        fid_gps.write(text)
        print(text)
        text = 'File name: ' + fileName
        fid_out.write(text)
        fid_gps.write(text)
        print(text)
        del text

        data_out = ''
        data_GPS = ''
        for line in fid_in:
            line = line.split('\t')
            if len(line) >= 1:
                data_out += line[0] + '\n'
            #if len(line) >= 3:
                #data_out.append('Date&Time: ' + line[1] + '\n')
                #data_out.append('Level: ' + line[2] + '\n')
            if len(line) > 3:
                data_GPS += 'GPS: ' + line[3]
                #line_gps = line[3].split(' ')
                #print('line_gps')
                #print(line_gps)
                #lat = float(line_gps[0])
                #long = float(line_gps[1])
                #height = float(line_gps[2])
                #speed = float(line_gps[3])
        print('\ndata_out')
        print(data_out)
        print('data_gps')
        print(data_GPS)
        fid_in.close()
        fid_out.write(data_out)
        fid_out.flush()
        fid_gps.write(data_GPS)
        fid_gps.flush()
    fid_out.close()
    fid_gps.close()
