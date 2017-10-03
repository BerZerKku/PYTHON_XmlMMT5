# -*- coding: utf-8 -*-
import sys
from distutils.core import setup
from glob import glob
import py2exe

# подключение библиотек Visual Studio
#sys.argv.append("py2exe")
sys.path.append("C:\\Python27\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Python27\Microsoft.VC90.CRT\*.*'))]

includes = ["sip"]
excludes = ['w9xpopen.exe']
packages = ['bisect']
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll', 'tk84.dll', 'w9xpopen.exe']

setup(
	# копирование библиотек Visual Studio
	data_files=data_files,
	#w9xpopen.exe - для совместимости с win 95/98
	#dll_excludes=['w9xpopen.exe'],
	# windows - GUI (может быть console)
	# icon_resources -> установка иконки для скомпилированного проекта
        windows=[{"script":"xmlMMT5_gui.py"}],
	#
        #options={"py2exe": {"includes":["sip"]}}
	options = {
            "py2exe": {
                "compressed": 2, 
		"optimize": 2,
		"includes": includes,
                "excludes": excludes,
                "packages": packages,
                "dll_excludes": dll_excludes,
                "bundle_files": 1,
                "dist_dir": "dist",
                "xref": False,
                "skip_archive": False,
                "ascii": False,
                "custom_boot_script": '',
            }
        },
	zipfile=None
)
