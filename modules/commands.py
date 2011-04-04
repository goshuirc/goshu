#!/usr/bin/env python3
"""
commands.py - Goshubot commands Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
from gbot.helper import splitnum

class Commands(Module):
	
	name = "Commands"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'quit' : [self.quit, 'quit', 10],
			},
		}
	
	def quit(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		(password, message) = splitnum(string)
		password = self.bot.encrypt(password)
		
		if self.bot.pass_hash == password:
			self.bot.irc.quit(server, message)
