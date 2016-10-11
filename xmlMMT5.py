# -*- coding: utf-8 -*-
from lxml import etree
import zipfile

FIELDS = ('ADDRESS', 'NAME')

TS32_K400_088_B = {}

##
def getNodesFromXml(name):
    ''' str -> list of lxml.etree._Element

        Возвращает содержимое XML файла (может быть сжат в zip) в виде
        списка элементов.
    '''

    try:
        archive = zipfile.ZipFile(name + '.zip', 'r')
        f = archive.open(name + '.XML')
    except:
        f = open(name + '.XML')
        

    parser = etree.XMLParser(encoding='utf-8')
    page = etree.parse(f, parser)
    nodes = page.xpath('/NODES/MASTERS/MASTER/POINTS/POINT')

    f.close()
    return nodes


##
def readXML(name, nodes, fields):
    ''' (str, list, dict) -> None

        Извлекаются поля согласно fields. Первое поле - ключевое.  
    '''
    print u"Адреса 104 протокола в %s." % (name)
    for node in nodes:
        key = node.get(fields[0])

        values = {}
        for i in range(1, len(fields)):
            values[fields[i]] = node.get(fields[i])
        
        globals()[name].update({key: values})


##
def printXML(name):
    ''' str -> None

        Вывод на экран отсортированного справочника \a name. 
    '''
    for key in sorted(eval(name)):
        print key,
        for value in eval(name)[key]:
            print '\t',
            print eval(name)[key].get(value),
        print


##
def saveFile(name):
    ''' (str) -> None

        Сохранение текстового файла.

        Запись производится по отсортированному словарю.
    '''
    f = open(name + '.txt', "w")

    for key in sorted(eval(name)):  
        s = str(key)
        for value in eval(name)[key]:
            s += '\t'
            s += eval(name)[key].get(value)
        s += '\n'
        f.write(s.encode('utf-8'))
    f.close()

          
##
if __name__ == "__main__":
    
    nodes = getNodesFromXml("TS32_K400-088-B")
    
    readXML("TS32_K400_088_B", nodes, FIELDS)
    printXML("TS32_K400_088_B")

    saveFile("TS32_K400_088_B")


      
