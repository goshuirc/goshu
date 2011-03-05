#!/usr/bin/env python
"""
bot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import os
import sys
import random

class Module(object):
	""" Basic class that adds some functionality/command to the Bot."""
	
	name = 'genericmodule'
	""" The name of the module."""
	
	def __init__(self):
		self.text_commands = {
			#'pubmsg' : { 'a' : self.acommand },
			#'privmsg' : { 'a' : self.acommand },
		}
		self.commands = {
			#'pubmsg' : self.stalk_convo,
		}

class ModuleLoader(object):
	""" Prepares a list of modules."""
	
	def __init__(self, path):
		self.run = random.randint(0, 10000)
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
			print 'ModuleLoader:', self.run, module.name #see whether both are
													#being bound in the same Loader
			yield module()
