#!/usr/bin/env python3
"""
modules.py - Goshubot modules Handler
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
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
	
	def __init__(self, bot):
		self.bot = bot
		self.events = {
			'in' : {},
			'out' : {},
			'commands' : {},
		}
		self.modules = {}
	
	def load(self, path):
		""" Loads modules in the given path."""
		loader = ModuleLoader(path)
		print (' '*self.bot.indent)+'Modules:'+(' '*(self.bot.indent-1)),
		for module in loader:
			self.append(module)
		print ''
	
	def append(self, module):
		""" Appends the given module to the handler."""
		self.modules[module.name] = module
		module.bot = self.bot
		for direction in module.events:
			for command in module.events[direction]:
				try:
					self.events[direction][command].append([module.name, module.events[direction][command]])
				except KeyError:
					self.events[direction][command] = [[module.name, module.events[direction][command]]]
		print module.name+' :',
	
	def handlers(self, direction, event):
		""" Returns a list of handlers of the given event."""
		handlers = []
		for handler in self.events[direction]:
			if handler == event:
				for function in self.events[direction][handler]:
					handlers.append(function[1])
			elif handler == 'all_events':
				for function in self.events[direction]['all_events']:
					handlers.append(function[1])
		return handlers
