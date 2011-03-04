#!/usr/bin/env python
"""
quit.py - Goshubot Quit Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.modules import Module

class Dice(Module):
	
	name = "Quit"
	
	def __init__(self):
		self.commands = {
			'q' : self.quit,
		}
		self.temp_password = hashlib.md5()
	
	def quit(self, password, connection, event):
		if password == '':
			connection.privmsg(event.source().split('!')[0], 'QUIT SYNTAX: .q <password>')
			return
		
		self.temp_password.update(password)
		if self.temp_password.digest() == self.gbot.password.digest():
			self.gbot.quit('QUIT')
		
		else:
			connection.privmsg(event.source().split('!')[0], 'QUIT: Password Incorrect')
