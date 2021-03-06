# -*- coding: utf-8 -*-
from lxml import etree
from argparse import ArgumentParser
from glob import glob
import sys, os, locale, shutil
import tarfile
import xlwt

# необходимые файлы в архиве MMT5
FILES = ('etc/KC/iec101_req.xml', 'etc/KC/iec104_serv.xml')
# необходимые поля таблиц
FIELDS = ('ADDRESS', 'NAME')

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
def getNodesFromXml(file):
    ''' file -> list of lxml.etree._Element

        Возвращает содержимое XML файла (может быть сжат в zip) в виде
        списка элементов.
    '''

    parser = etree.XMLParser(encoding='utf-8')
    page = etree.parse(file, parser)
    # строка для поиска в 'iec104_serv.xml'
    nodes = page.xpath('/NODES/MASTERS/MASTER/POINTS/POINT')
    # строка для поиска в 'iec101_req.xml'
    if len(nodes) == 0:
        nodes = page.xpath('/NODES/SLAVES/SLAVE/DEVICES/DEVICE/POINTS/POINT')

    return nodes


##
def readXML(nodes, fields, table):
    ''' (list, dict, dict) -> None

        Извлекаются поля согласно fields. Первое поле - ключевое.  
    '''
    
    for node in nodes:
        key = node.get(fields[0])

        values = {}
        for i in range(1, len(fields)):
            values[fields[i]] = node.get(fields[i])
        
        table.update({key: values})


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
    
    ws.write(0, 0, unicode(FIELDS[0]))
    ws.write(0, 1, unicode(FIELDS[1]))
    i = 1
    for key in sorted(table, key=my_key):
        ws.write(i, 0, unicode(key))
        s = ''
        for value in table[key]:
            s += table[key].get(value)
        ws.write(i, 1, unicode(s))
        i += 1
    wr_wb.save(unicode(fname.rsplit('.', 1)[0] + '.xls'))
        

##
def saveFile(fname, table):
    ''' (str, str) -> None

        Сохранение в текстовый файл \a fname данных из таблицы \a table.

        Запись производится по отсортированному словарю.
    '''

    f = open(fname.rsplit('.', 1)[0] + '.txt', "w")

    s = FIELDS[0].rjust(10) + '  ' + FIELDS[1] + '\n'
    f.write(s.encode('utf-8'))
    
    for key in sorted(table, key=my_key):
        s = key.rjust(10)
        s += '  '
        for value in table[key]:
            s += table[key].get(value)
        s += '\n'
        f.write(s.encode('utf-8'))
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
    except KeyError, err:
        print 'ERROR file %s: %s' % (fname, err)
        return False
    except IOError, err:
        print 'ERROR file %s: %s' % (fname, err)
        return False
    
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
            saveTableToFile(moveto)
            # удаляем файл
            os.remove(moveto)
        except KeyError, err:
            print 'ERROR file %s: %s' % (fname, err)
            return False
            
    os.remove(farchive)
    return True

##
def saveTableToFile(fname):
    ''' (str) -> Bool

        Сохраняет необходимые данные в файл '*.txt'.
        
        Возвращает True в случае удачного сохранения файла. Иначе False.
    '''

    try:
        f = open(fname)
    except:
        print "File %s error." % (fname)
        return False

    table = {}
    nodes = getNodesFromXml(f)
    readXML(nodes, FIELDS, table)
    saveXML(fname, table)
    saveFile(fname, table)
    f.close()
    return True
          
##
if __name__ == "__main__":

    # проверка наличия входных данных
    if len(sys.argv) < 2:
        print "File not found."
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
        print 'File Type "*.%s" not supported.' % (file_ext)
        sys.exit()
