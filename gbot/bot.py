#!/usr/bin/env python3
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot	-	http://danneh.net/goshu

from . import info, irc, modules

DEBUG = False

class Bot:
	"""Brings all of goshubot together in a nice happy class."""
	
	def __init__(self):
		self.DEBUG = DEBUG
		
		self.settings = info.Settings(self)
		self.info = info.Info(self)
		self.irc = irc.IRC(self)
		self.modules = modules.Modules(self)
	
	def start(self):
		self.irc.add_handler('all', 'all', self.modules.handle)
		self.irc.connect_info(self.info, self.settings)
		self.irc.process_forever()