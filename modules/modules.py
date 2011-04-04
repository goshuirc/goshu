#!/usr/bin/env python3
"""
modules.py - Goshubot module control Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module

class Modules(Module):
	
	name = "Modules"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'list' : [self.list_commands, 'lists avaliable commands', 0],
			},
		}
	
	def list_commands(self, args, connection, event):
		server = self.bot.irc.server_nick(connection)
		nick = event.source().split('!')[0]
		
		largest_length = 0
		for command in self.bot.modules.events['commands']:
			if self.bot.access(nick) >= self.bot.modules.events['commands'][command][0][1][2]:
				if len(command) > largest_length:
					largest_length = len(command)
		
		self.bot.irc.privmsg(server, nick, 'Command List:')
		for command in self.bot.modules.events['commands']:
			if self.bot.access(nick) >= self.bot.modules.events['commands'][command][0][1][2]:
				indent = largest_length - len(command)
				indent = ' ' * indent
				output = self.bot.indent * ' '
				output += self.bot.prefix
				output += command
				output += indent
				output += ' : '
				output += self.bot.modules.events['commands'][command][0][1][1]
				self.bot.irc.privmsg(server, nick, output)
