# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
import ttk
from xmlMMT5 import extractMMT5files

# имя файла
fn = ''

root = Tk()

print 'Run!'

def LoadFile():
    global fn
    fn = tkFileDialog.Open(root, filetypes = [('MT-500 backup', '.tar')]).show()
    # проверка выбранного файла
    if (fn == '') or (fn.rsplit('.',1)[-1] != 'tar'):
        btn2.configure(state=DISABLED)
        return

    btn2.configure(state=NORMAL)
    extractMMT5files(fn)

def Extract():
    extractMMT5files(fn)

btn1 = ttk.Button(root, text="Открыть файл", width=30, command=LoadFile)
btn1.pack()

btn2 = ttk.Button(root, text=u"Извлечь данные", width=30, command=Extract)
btn2.configure(state=DISABLED)
btn2.pack()

root.mainloop()

