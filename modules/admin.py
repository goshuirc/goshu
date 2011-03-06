#!/usr/bin/env python
"""
admin.py - Goshubot Administration Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.helper import splitnum
from gbot.modules import Module

class Admin(Module):
	
	name = "Admin"
	
	def __init__(self):
		self.text_commands = {
			'privmsg' : { 
				'op' : self.op,
			},
			'pubmsg' : { 
				'op' : self.op,
			},
		}
		self.commands = {}
	
	def op(self, line, connection, event):
		if line == None and connection == None and event == None:
			text_commands_info = {
				"op owner" : [0, 0, 'make yourself a bot owner'],
			}
			return (text_commands_info)
			
		try:
			(command, line) = splitnum(line)
		except:
			output = 'OP: Command Failed'
			
			connection.privmsg(event.source().split('!')[0], output)
			return
		
		if command == 'owner':
			password = line
			
			if self.gbot.is_password(password):
				pass
