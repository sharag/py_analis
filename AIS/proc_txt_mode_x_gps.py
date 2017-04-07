#!/usr/bin/python3.5
# Вырезает из демодулированных файлов отдельно сообщения для shipplotter
# и отдельно данные GPS
import sys
import glob
import argparse
import numpy as np


class GpsInterp:

    def __init__(self):
        self.gps_data = []
        self.first_data = 0
        self.last_data = 0

    def add_data(self, lat_, long_, height_, speed_):
        self.gps_data.append([lat_, long_, height_, speed_])
        if lat_ != 0.0:
            self.last_data = len(self.gps_data)
            if self.first_data == 0 or (self.last_data - self.first_data) == 1:
                self.first_data = len(self.gps_data)
            else:
                lat_array = np.linspace(self.gps_data[self.first_data - 1][0], self.gps_data[self.last_data - 1][0],
                                        self.last_data - self.first_data + 1)[1:-1]
                long_array = np.linspace(self.gps_data[self.first_data - 1][1], self.gps_data[self.last_data - 1][1],
                                         self.last_data - self.first_data + 1)[1:-1]
                height_array = np.linspace(self.gps_data[self.first_data - 1][2], self.gps_data[self.last_data - 1][2],
                                           self.last_data - self.first_data + 1)[1:-1]
                speed_array = np.linspace(self.gps_data[self.first_data - 1][3], self.gps_data[self.last_data - 1][3],
                                          self.last_data - self.first_data + 1)[1:-1]
                for k in range(self.last_data - self.first_data - 1):
                    self.gps_data[self.first_data + k][0] = lat_array[k]
                    self.gps_data[self.first_data + k][1] = long_array[k]
                    self.gps_data[self.first_data + k][2] = height_array[k]
                    self.gps_data[self.first_data + k][3] = speed_array[k]
                self.first_data = len(self.gps_data)


    def get_data(self):
        return self.gps_data


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    parser_.add_argument('-r', '--recursive', nargs='?', help='Search recursive in input directory: -r', default=False)
    return parser_


if __name__ == '__main__':
    parser = create_parser()
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
        filesList = glob.glob(namespace.inpath + '*.ais')
    print('Path: ' + namespace.inpath)
    if len(filesList) < 1:
        raise BaseException('Infile not exist.')
    numfile = 0
    gps_interp = None
    fid_out = open(namespace.inpath + 'result.out', 'w')
    fid_gps = open(namespace.inpath + 'result.gps', 'w')
    for fileName in filesList:
        numfile += 1
        fid_in = open(fileName, 'r')
        gps_interp = GpsInterp()

        text = '\nFile number: ' + str(numfile) + '/' + str(len(filesList)) + '\n'
        fid_out.write(text)
        fid_gps.write(text)
        print(text)
        text = 'File name: ' + fileName + '\n'
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
            # if len(line) >= 3:
                # data_out.append('Date&Time: ' + line[1] + '\n')
                # data_out.append('Level: ' + line[2] + '\n')
            if len(line) > 3:
                line_gps = line[3].split(' ')
                if len(line_gps) == 4:
                    gps_interp.add_data(float(line_gps[0]), float(line_gps[1]), float(line_gps[2]), float(line_gps[3]))
                else:
                    gps_interp.add_data(float(line_gps[0]), float(line_gps[1]), 0.0, float(line_gps[2]))
                # lat = float(line_gps[0])
                # long = float(line_gps[1])
                # height = float(line_gps[2])
                # speed = float(line_gps[3])
        data_GPS = gps_interp.get_data()
        for j in range(len(data_GPS)):
            for l in range(len(data_GPS[j])):
                data_GPS[j][l] = '{0:10.6f}'.format(float(data_GPS[j][l])).replace(' ', '0')
            data_GPS[j] = ' '.join(data_GPS[j])
        data_GPS = '\n'.join(data_GPS)
        print('\ndata_out')
        print(data_out)
        print('data_gps')
        print(data_GPS)
        fid_in.close()
        fid_out.write(data_out)
        fid_out.flush()
        fid_gps.write(data_GPS)
        fid_gps.flush()
        gps_interp = None
    fid_out.close()
    fid_gps.close()
