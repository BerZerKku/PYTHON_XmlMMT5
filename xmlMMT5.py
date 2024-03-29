# -*- coding: utf-8 -*-
from lxml import etree
from argparse import ArgumentParser
from glob import glob
import sys, os, locale, shutil
import tarfile
import xlwt
import six


# необходимые файлы в архиве MMT5
FILES = ('etc/KC/iec101_req.xml', 'etc/KC/iec104_serv.xml')
# необходимые поля таблиц
FIELDS = ('ADDRESS', 'NAME')
# файл с именами сигналов
WAREHOUSE = ('etc/KC/warehouse.xml')

##
def my_key(dict_key):
    ''' (str) -> int

        Возвращает значение int полученное из строки.
        Используется для нормальной сортировки числовых массивов.
    '''

    try:
        return int(dict_key)
    except ValueError:
        return dict_key

##
def readWarehouseNames(file_name):
    ''' str -> list

        Получает список элементов из общего хранилища.
    '''
    enames = {}

    try:
        file = open(file_name, encoding='utf-8')

        parser = etree.XMLParser()
        page = etree.parse(file, parser)

        # строка для поиска в 'iec104_serv.xml'
        nodes = page.xpath('/KERNEL/POINTS/POINT')

        for node in nodes:
            key = node.get("NAME")
            value = node.get("NAMING")
            if (not (key is None)) and (not (value is None)):
                enames[key] = value

    except Exception as e:
        print ("ERROR File {0} error: {1}.".format(file_name, e))
        return dict()

    return enames

##
def getNodesFromXml(file):
    ''' file -> list of lxml.etree._Element

        Возвращает содержимое XML файла (может быть сжат в zip) в виде
        списка элементов.
    '''

    parser = etree.XMLParser()
    page = etree.parse(file, parser)
    # строка для поиска в 'iec104_serv.xml'
    nodes = page.xpath('/NODES/MASTERS/MASTER/POINTS/POINT')
    # строка для поиска в 'iec101_req.xml'
    if len(nodes) == 0:
        nodes = page.xpath('/NODES/SLAVES/SLAVE/DEVICES/DEVICE/POINTS/POINT')

    return nodes


##
def readXML(nodes, wnames, fields):
    ''' (list, dict, tuple) -> None

        nodes - список элементов
        wnames - словарь эелементов и их названий
        fields - поля которые надо извлечь

        Извлекаются поля согласно fields. Первое поле - ключевое.
    '''

    table = dict()

    for node in nodes:
        key = node.get(fields[0])

        values = {}
        for i in range(1, len(fields)):
            field = fields[i]
            value = node.get(field)
            if (field == "NAME") and value.startswith("LOC.") and (value in wnames):
                value += ' ' + wnames[value]
            values[field] = value

        table.update({key: values})

    return table


##
def saveXML(fname, table):
    ''' (str, str) -> None

        Сохранение в '*.xls' файл \a fname данных из таблицы \a table.

        Запись производится по отсортированному словарю.
    '''

    # созданим новый файл
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    wr_wb = xlwt.Workbook()
    ws = wr_wb.add_sheet(u'Адрес')

    ws.write(0, 0, six.text_type(FIELDS[0]))
    ws.write(0, 1, six.text_type(FIELDS[1]))
    i = 1
    for key in sorted(table, key=my_key):
        ws.write(i, 0, six.text_type(key))
        s = ''
        for value in table[key]:
            s += table[key].get(value)
        ws.write(i, 1, six.text_type(s))
        i += 1
    wr_wb.save(six.text_type(fname.rsplit('.', 1)[0] + '.xls'))


##
def saveFile(fname, table):
    ''' (str, str) -> None

        Сохранение в текстовый файл \a fname данных из таблицы \a table.

        Запись производится по отсортированному словарю.
    '''

    f = open(fname.rsplit('.', 1)[0] + '.txt', "w")

    s = FIELDS[0].rjust(10) + '  ' + FIELDS[1] + '\n'
    f.write(s)

    for key in sorted(table, key=my_key):
        s = key.rjust(10)
        s += '  '
        for value in table[key]:
            s += table[key].get(value)
        s += '\n'
        f.write(s)
    f.close()


##
def extractMMT5files(fname):
    ''' (str, list of str) -> Bool

        Извлекает из файла fname нужные файлы.

        Возвращает False в случае ошибки и True, если все нормально.
    '''

    farchive = 'package.tar.gz'

    # извлекаем первый архив
    try:
        tar = tarfile.open(fname, 'r')
        tar.extract(farchive, '.')
        tar.close()
    except Exception as e:
        print ("ERROR File {0} error: {1}.".format(file_name, e))
        return False

    wnames = {}

   # извлекаем сигналы из общего хранилища
    try:
        tar = tarfile.open(farchive, 'r:gz')
        tar.extract(WAREHOUSE, '')
        tar.close()
        moveto = WAREHOUSE.rsplit('/', 1)[-1]
        # переносим файл в текущую папку
        shutil.move('./' + WAREHOUSE, moveto)
        # удаялем созданную папку
        shutil.rmtree('./' + WAREHOUSE.rsplit('/')[0], ignore_errors=False, onerror=None)
        # сохраняем таблицу
        wnames = readWarehouseNames(moveto)
        # удаляем файл
        os.remove(moveto)
    except Exception as e:
        print ("ERROR File {0} error: {1}.".format(fname, e))


    # извлекаем нужные файлы
    for f in FILES:
        try:
            tar = tarfile.open(farchive, 'r:gz')
            tar.extract(f, '')
            tar.close()
            moveto = f.rsplit('/', 1)[-1]
            # переносим файл в текущую папку
            shutil.move('./' + f, moveto)
            # удаялем созданную папку
            shutil.rmtree('./' + f.rsplit('/')[0], ignore_errors=False, onerror=None)
            # сохраняем таблицу
            saveTableToFile(moveto, wnames)
            os.remove(moveto)
        except Exception as e:
            print ("ERROR File {0} error: {1}.".format(fname, e))
            return False

    os.remove(farchive)
    return True

##
def saveTableToFile(fname, wnames={}):
    ''' (str, dict) -> Bool

        Сохраняет необходимые данные в файл '*.txt'.

        Возвращает True в случае удачного сохранения файла. Иначе False.
    '''

    try:
        f = open(fname, encoding='utf-8')
    except:
        print("File %s error." % (fname))
        return False

    table = {}
    nodes = getNodesFromXml(f)
    table = readXML(nodes, wnames, FIELDS)

    saveXML(fname, table)
    saveFile(fname, table)

    f.close()
    return True

##
if __name__ == "__main__":

    # проверка наличия входных данных
    if len(sys.argv) < 2:
        print("File not found.")
        sys.exit()

    # имя файла+расширение
    file_name_ext = sys.argv[1]

    # имя файла
    file_name = file_name_ext.rsplit('.', 1)[0]

    # расширение файла
    file_ext = file_name_ext.split('.')[-1].lower()


    if file_ext == 'xml':
        saveTableToFile(file_name_ext)
    elif file_ext == 'tar':
        if not extractMMT5files(file_name_ext):
            sys.exit()
    else:
        print('File Type "*.%s" not supported.'%(file_ext))
        sys.exit()
