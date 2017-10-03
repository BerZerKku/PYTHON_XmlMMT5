# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe, sys, os

setup(
        
	options = {
		'py2exe': {
			'bundle_files': 3, 
			'compressed': True,
			'includes': ['lxml.etree', 'lxml._elementpath']
		}
	},
    windows = [{'script':'xmlMMT5_gui.py'}],
	zipfile = None
)
