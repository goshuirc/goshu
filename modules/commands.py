#!/usr/bin/env python
"""
commands.py - Goshubot Commands Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

from gbot.modules import Module

class Commands(Module):
	
	name = "Commands"
	
	def __init__(self):
		self.commands = {
			'list' : self.list,
		}
	
	def list(self, line, connection, event):
		connection.privmsg(event.source().split('!')[0], 'COMMANDS:')
		for alias in self.gbot.commands:
			connection.privmsg(event.source().split('!')[0], '    '+self.gbot.prefix + alias)
