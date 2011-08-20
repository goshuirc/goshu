#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot	-	http://danneh.net/goshu
import os
import sys

class Module:
	"""Module to add commands/functionality to the bot."""
	...

class ModuleLoader:
	"""Prepares a list of modules."""
	
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

class Modules:
	"""Manages goshubot's modules."""
	
	def __init__(self, bot):
		self.bot = bot
		self.modules = {}
		self.handlers = {}
	
	def load(self, path):
		loader = ModuleLoader(path)
		output = 'modules '
		for module in loader:
			if self.append(module):
				output += module.name + ', '
		output = output[:-2]
		output += ' loaded'
		print(output)
	
	def append(self, module):
		if module not in self.modules:
			self.modules[module.name] = module
			for direction in ['in', 'out', 'commands', 'all']:
				if direction not in module.events:
					module.events[direction] = {}
			self.handlers[module.name] = module.events
			module.bot = self.bot
			return True
		else:
			return False
	
	def handle(self, event):
		called = []
		for module in self.handlers:
			if event.type in self.handlers[module][event.direction]:
				for h in self.handlers[module][event.direction][event.type]:
					if h[1] not in called:
						called.append(h[1])
						h[1](event)
			if 'all' in self.handlers[module][event.direction]:
				for h in self.handlers[module][event.direction]['all']:
					if h[1] not in called:
						called.append(h[1])
						h[1](event)
			if event.type in self.handlers[module]['all']:
				for h in self.handlers[module]['all'][event.type]:
					if h[1] not in called:
						called.append(h[1])
						h[1](event)
			if 'all' in self.handlers[module]['all']:
				for h in self.handlers[module]['all']['all']:
					if h[1] not in called:
						called.append(h[1])
						h[1](event)
		if event.type == 'privmsg' or event.type == 'pubmsg':
			self.handle_command(event)
	
	def handle_command(self, event):
		if event.arguments[0].split(self.bot.settings._store['prefix'])[0] == '':
			if len(event.arguments[0].split(self.bot.settings._store['prefix'])[1].strip()) < 1:
				return # empty
			elif len(event.arguments[0].split(self.bot.settings._store['prefix'])[1].split()[0]) < 1:
				return # no command
			command_name = event.arguments[0][1:].split()[0]
			try:
				command_args = event.arguments[0][1:].split(' ', 1)[1]
			except IndexError:
				command_args = ''
			called = []
			for module in self.handlers:
				if 'commands' in self.handlers[module]:
					try:
						self.handlers[module]['commands'][command_name][0](event, Command(command_name, command_args))
					except KeyError:
						...

class Command:
	"""Command from a client."""
	
	def __init__(self, command, arguments):
		self.command = command
		self.arguments = arguments