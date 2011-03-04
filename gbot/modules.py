#!/usr/bin/env python
"""
bot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import os
import sys

class Module(object):
	""" Basic class that adds some functionality/command to the Bot."""
	
	name = 'genericmodule'
	""" The name of the module."""
	alias = ''
	""" The letter/word the module responds to."""
	
	def __init__(self):
		""" The letter/word the module responds to."""

class ModuleLoader(object):
	""" Prepares a list of scenes for Bot to load."""
	
	def __init__(self, path):
		self.path = path
	
	def __iter__(self):
		for(dirpath, dirs, files) in os.walk(self.path):
			if not dirpath in sys.path:
				sys.path.insert(0, dirpath)
			for file in files:
				(name, ext) = os.path.splitext(file)
				if ext == os.extsep + 'py':
					__import__(name, None, None, [''])
		for module in Module.__subclasses__():
			yield module()
