#!/usr/bin/env python
"""
modules.py - Goshubot modules Handler
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

import os
import sys

class Module(object):
	""" Basic class that adds functionality/commands to the Bot."""
	
	name = 'Example'
	
	def __init__(self):
		self.events = {
			'in' : {
				#'privmsg'
			},
			'out' : {
			
			},
			'commands' : {
				#'8ball' : self.ask,
			},
		}

class ModuleLoader(object):
	""" Prepares a list of modules."""
	
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

class ModuleHandler(object):
	""" Handles Modules."""
	
	def __init__(self):
		self.events = {}
		self.modules = {}
	
	def load(self, path):
		""" Loads modules in the given path."""
		loader = ModuleLoader(path)
		for module in loader:
			self.append(module)
	
	def append(self, module):
		""" Appends the given module to the handler."""
		self.modules[module.name] = module
		print module.name, 'has been loaded'
