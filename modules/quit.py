#!/usr/bin/env python
"""
quit.py - Goshubot Quit Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.modules import Module

class Quit(Module):
	
	name = "Quit"
	
	def __init__(self):
		self.text_commands = {
			'pubmsg' : { 'q' : self.quit },
			'privmsg' : { 'q' : self.quit },
		}
		self.commands = {}
	
	def quit(self, password, connection, event):
		if password == '':
			connection.privmsg(event.source().split('!')[0], 'QUIT SYNTAX: .q <password>')
			return
		
		if hashlib.sha512(password).hexdigest() == self.gbot.password.hexdigest():
			self.gbot.quit('QUIT issued by '+event.source().split('!')[0])
		
		else:
			connection.privmsg(event.source().split('!')[0], 'QUIT: Password Incorrect')
