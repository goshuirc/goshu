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
	
	def __init__(self, nick='goshu', prefix='.', indent=3, module_path='modules'):
		self.nick = nick
		self.prefix = prefix
		self.indent = indent
		
		self.irc = irc.IRC(self)
		self.modules = modules.ModuleHandler(self)
		
		#setting up links to each-other
		self.irc.modules = self.modules
		self.modules.irc = self.irc
		
		self.modules.load(module_path)
	
	def prompt_settings(self, current_settings=None):
		""" Prompts user for global bot settings."""
		try:
			current_nick = current_settings['nick']
			nick = raw_input((' '*self.indent)+'Nick ['+current_nick+']: ').split(' ')[0]
			if nick == '':
				nick = current_nick
		except:
			nick = raw_input((' '*self.indent)+'Nick: ').split(' ')[0]
		
		return {
			'nick' : nick,
		}
	
	def process_settings(self, settings):
		""" Sets the settings defined by the given dictionary."""
		self.nick = settings['nick']
