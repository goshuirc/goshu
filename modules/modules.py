#!/usr/bin/env python
"""
modules.py - Goshubot Module Command Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

from gbot.modules import Module

class Modules(Module):
	
	name = "Modules"
	
	def __init__(self):
		self.text_commands = {
			'privmsg' : { 
				'list' : self.list_commands,
			},
			'pubmsg' : { 
				'list' : self.list_commands,
			},
		}
		self.commands = {}
	
	def list_commands(self, line, connection, event):
		if line == None and connection == None and event == None:
			text_commands_info = {
				"list" : [0, 0, 'lists bot commands'],
			}
			return (text_commands_info)
		
		largest_length = 0
		for command in self.gbot.text_commands_info: # length/indent of commands
			if len(command) > largest_length:
				largest_length = len(command)
		
		connection.privmsg(event.source().split('!')[0], 'Command List:')
		for command in self.gbot.text_commands_info:
			if self.gbot.level(event.source()) >= self.gbot.text_commands_info[command][0]:
				indent = largest_length - len(command)
				indent = ' ' * indent
				output = str(' '+self.gbot.prefix+command+indent+' : '+self.gbot.text_commands_info[command][2])
				connection.privmsg(event.source().split('!')[0], output)
