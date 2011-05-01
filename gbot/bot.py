#!/usr/bin/env python3
"""
bot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

import hashlib
import getpass

from . import irc
from . import modules
from . import data
from . import strings

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
			nick = input((' '*self.indent)+'Nick ['+current_nick+']: ').split(' ')[0]
			if nick == '':
				nick = current_nick
		except:
			nick = input((' '*self.indent)+'Nick: ').split(' ')[0]
		
		
		get_new_pass = ''
		try:
			current_pass_hash = current_settings['pass_hash']
			get_new_pass = ''
			while get_new_pass != 'n' and get_new_pass != 'y':
				get_new_pass = input((' '*self.indent)+'New Password? ')[0]
		except:
			get_new_pass = 'y'
		
		if get_new_pass == 'y':
			new_pass = getpass.getpass((' '*self.indent)+'Password: ')
			pass_hash = self.encrypt(new_pass.encode('utf8'))
		else:
			pass_hash = current_settings['pass_hash']
		
		
		return {
			'nick' : nick,
			'pass_hash' : pass_hash,
		}
	
	def process_settings(self, settings):
		""" Sets the settings defined by the given dictionary."""
		self.nick = settings['nick']
		self.pass_hash = settings['pass_hash']
	
	
	def access(self, nick):
		""" Supposed to return the access level of the given nick."""
		return 0
	
	def encrypt(self, password):
		""" Encrypt and return given password."""
		return hashlib.sha512(password).hexdigest()
