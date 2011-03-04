#!/usr/bin/env python
"""
quit.py - Goshubot Quit Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

from gbot.modules import Module

class Dice(Module):
	
	name = "Quit"
	
	def __init__(self):
		self.password = 'moemoekyun'
		self.commands = {
			'q' : self.quit,
		}
	
	def quit(self, line, connection, event):
		if line == '':
			connection.privmsg(event.source().split('!')[0], 'QUIT SYNTAX: .q <password>')
			return
		
		if line == self.password:
			self.gbot.quit('QUIT')
