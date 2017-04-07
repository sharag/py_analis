#!/usr/bin/python3.5
""""Исследование деможулятора.
Вход:
-i <Путь к каталогу с файлами *.iq или непосредственно путь к файлу (обязательный параметр)>
-d <путь к исполняемому файлу демодулятора (обязательный параметр)>
-r <если указан данный параметр и параметр -i - каталог, 
    то будут просмотрены все каталоги рекурсивно> (необязательный параметр)"""
import sys
import glob
import argparse
import os
from subprocess import Popen, PIPE
import numpy as np
import time


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    parser_.add_argument('-r', '--recursive', nargs='?', help='Search recursive in input directory: -r', default=False)
    parser_.add_argument('-d', '--demodpath', nargs='+', help='Path to the demod file: -d <path>')
    return parser_


def create_temp_file(file_name):
    """Функция создает новый временный файл для демодулятора и аозвращает его имя."""
    if os.path.getsize(file_name) > 97867090:  # минута - 280 Мб, 20 сек - примерно 94 Мб
        num_temp_file = 0
        while True:
            if os.path.exists(file_name + '.tmp' + str(num_temp_file) + '.iq'):
                num_temp_file += 1
            else:
                fname_temp_ = file_name + '.tmp' + str(num_temp_file) + '.iq'
                break
        fid_in = open(file_name, 'rb')
        data_raw = fid_in.read(97867090)
        fid_in.close()
        fid_in = open(fname_temp_, 'wb')
        fid_in.write(data_raw)
        fid_in.close()
        del fid_in, data_raw, num_temp_file
    else:
        num_temp_file = 0
        while True:
            if os.path.exists(file_name + '.tmp' + str(num_temp_file) + '.iq'):
                num_temp_file += 1
            else:
                fname_temp_ = file_name + '.tmp' + str(num_temp_file) + '.iq'
                break
        fid_in = open(file_name, 'rb')
        data_raw = fid_in.read()
        fid_in.close()
        fid_in = open(fname_temp_, 'wb')
        fid_in.write(data_raw)
        fid_in.close()
        del fid_in, data_raw, num_temp_file
    return fname_temp_


def write_state(f_name_, txt):
    """Функция открывает файл состония для записи с добавлением.
    Если файл не удается открыть (например потому, что он занят другим процессом) функция ждет)"""
    f_name_st = f_name_[0:-2] + 'st'
    while True:
        try:
            fid_st = open(f_name_st, 'a')
            fid_st.write(txt)
            fid_st.close()
            break
        except OSError:
            time.sleep(0.1)
            print('File state busy... Waiting for write.')
            continue
    return


def read_state(pll_gain_, in_lpf_, dc_lpf_, file_name):
    """Функция проверяет существование файла состония, если он существует читает его и определяет, был уже такой 
    эксперимент или нет. Если Эксперимента не было, или файл состояния не существует, выдает True. Иначе - False.
    Если файл не удается открыть (например потому, что он занят другим процессом) функция ждет)"""
    f_name_st = file_name[0:-2] + 'st'
    if os.path.exists(f_name_st):
        while True:
            try:
                fid_st = open(f_name_st, 'r')
                array_pll_gain = []
                array_in_lpf_ = []
                array_dc_lpf_ = []
                # Чтение массива
                for line_ in fid_st:
                    if line_.find('Current') >= 0:
                        array_pll_gain.append(float(line_.split('\t')[1].split(':')[1]))
                        array_in_lpf_.append(float(line_.split('\t')[2].split(':')[1]))
                        array_dc_lpf_.append(float(line_.split('\t')[3].split(':')[1]))
                fid_st.close()
                break
            except OSError:
                time.sleep(0.1)
                print('File state busy... Waiting for read.')
                continue
        indexes_pll_gain = [ind for ind, x in enumerate(array_pll_gain) if x == pll_gain_]
        indexes_in_lpf_ = [x for x in indexes_pll_gain if array_in_lpf_[x] == in_lpf_]
        indexes_dc_lpf = [x for x in indexes_in_lpf_ if array_dc_lpf_[x] == dc_lpf_]
        if len(indexes_dc_lpf) > 0:
            return False
        else:
            return True
    else:
        return True


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
    demodpath = namespace.demodpath[0]
    if len(namespace.demodpath) > 1:
        for i in range(1, len(namespace.demodpath)):
            demodpath += ' ' + namespace.demodpath[i]
    namespace.demodpath = demodpath
    del demodpath
    if os.path.exists(namespace.inpath) and os.path.isfile(namespace.inpath):
        filesList = [namespace.inpath]
    else:
        if namespace.recursive:
            filesList = glob.glob(namespace.inpath + '**//*.iq', recursive=True)
        else:
            filesList = glob.glob(namespace.inpath + '*.iq', recursive=False)
    if len(filesList) < 1:
        raise BaseException('In the catalog a little of files.')
    filesList.sort()
    numfile = 0
    for fileName in filesList:
        numfile += 1
        text = ''
        # Формирование кусочка файла для обработки
        fname_temp = create_temp_file(fileName)
        print('\nNumber:' + str(numfile) + '/' + str(len(filesList)) + '\n')
        text += 'Name:' + fileName + '\n'
        print('Name:' + fileName + '\n')
        # Формирование массивов для проведения измерений
        pll_gain_array = [x for x in range(4, 32)]
        pll_gain_array += [x for x in range(32, 128, 4)]
        print('Number pll_gain: ' + str(len(pll_gain_array)))
        in_lpf_array = [x for x in np.arange(0.4, 0.54, 0.01)]
        in_lpf_array += [x for x in np.arange(0.54, 0.9, 0.01)]
        print('Number in_lpf: ' + str(len(in_lpf_array)))
        dc_lpf_array = [0.016, 0.018]
        dc_lpf_array += [x for x in np.arange(0.019, 0.024, 0.001)]
        dc_lpf_array += [x for x in np.arange(0.024, 0.042, 0.002)]
        dc_lpf_array += [x for x in np.arange(0.19, 0.22, 0.005)]
        print('Number dc_lpf: ' + str(len(dc_lpf_array)))
        # Номинальные значения: pll_gain = 8 in_lpf = 0.48 dc_lpf = 0.02
        max_num_mes = [0, 0, 0, 0]
        experiment_num = 0
        all_exp_num = len(pll_gain_array) * len(in_lpf_array) * len(dc_lpf_array)
        # Начинаем эксперименты
        for pll_gain in pll_gain_array:
            for in_lpf in in_lpf_array:
                for dc_lpf in dc_lpf_array:
                    # Если этот эксперимент уже проводился, то переходим к следующему
                    if not read_state(pll_gain, in_lpf, dc_lpf, fileName):
                        experiment_num += 1
                        print('Experiment passed:\tpll_gain:' + str(pll_gain) + '\tin_lpf:' + str(in_lpf) + '\tdc_lpf:'
                              + str(dc_lpf) + '\tnum_message:' + str(num_message) + '\n')
                        continue
                    num_message = 0
                    num = 0
                    experiment_num += 1
                    print('\nExperiment number: ' + str(experiment_num) + '/' + str(all_exp_num) + '\n')
                    child_proc = Popen([namespace.demodpath, '-v', '-m', str(pll_gain), '-o', str(in_lpf), '-d',
                                        str(dc_lpf), '-F', '2400000', '-f', fname_temp, '162050', '161975', '162025'],
                                       stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
                    [out_bytes, err_bytes] = child_proc.communicate(timeout=3600)
                    out_txt = out_bytes.decode('utf-8')
                    err_txt = err_bytes.decode('utf-8')
                    # Разбор сообщения демодулятора (а точнее stderr)
                    for line in err_txt.split('\n'):
                        if line.find('Ch') >= 0:
                            print('line: ' + line)
                            num_message += int(line[(line.find('get') + 4):(-1)].split(',')[0])
                    if max_num_mes[3] < num_message:
                        max_num_mes = [pll_gain, in_lpf, dc_lpf, num_message]
                    # Сообщения
                    text += 'Current:\tpll_gain:' + str(pll_gain) + '\tin_lpf:' + str(in_lpf) + '\tdc_lpf:' + \
                            str(dc_lpf) + '\tnum_message:' + str(num_message) + '\n'
                    print('Current:\tpll_gain:' + str(pll_gain) + '\tin_lpf:' + str(in_lpf) + '\tdc_lpf:' + str(dc_lpf)
                          + '\tnum_message:' + str(num_message) + '\n')
                    print('Old max:\tpll_gain:' + str(max_num_mes[0]) + '\tin_lpf:' + str(max_num_mes[1]) + '\tdc_lpf:'
                          + str(max_num_mes[2]) + '\tnum_message:' + str(max_num_mes[3]) + '\n')
                    write_state(fileName, text)
                    text = ''
        text += '\n\n\nWork complete!!!'
        print('\n\n\nWork complete!!!')
        text += 'Old max:\tpll_gain:' + str(max_num_mes[0]) + '\tin_lpf:' + str(max_num_mes[1]) + '\tdc_lpf:' + \
                str(max_num_mes[2]) + '\tnum_message:' + str(max_num_mes[3]) + '\n'
        print('Old max:\tpll_gain:' + str(max_num_mes[0]) + '\tin_lpf:' + str(max_num_mes[1]) + '\tdc_lpf:' +
              str(max_num_mes[2]) + '\tnum_message:' + str(max_num_mes[3]) + '\n')
        write_state(fileName, text)
        text = ''
