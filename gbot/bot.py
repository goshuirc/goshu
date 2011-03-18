#!/usr/bin/env python
"""
bot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

import irc
import modules
import data

class Bot(object):
	""" Brings everything together."""
	
	def __init__(self, prefix='.', indent=3, module_path='modules'):
		self.irc = irc.IRC()
		self.modules = modules.ModuleHandler()
		
		#setting up links to each-other
		self.irc.modules = self.modules
		self.modules.irc = self.irc
		
		self.modules.load(module_path)
