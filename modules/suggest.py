#!/usr/bin/env python3
"""
suggest.py - Goshubot suggest Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module
from gbot.helper import splitnum
import string

class Suggest(Module):
	
	name = "Suggest"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'suggest' : [self.suggest, 'suggest something to goshubot', 0],
			},
		}
		
		self.valid_characters = string.ascii_letters + string.digits + '-_ []{}!^#'
	
	def suggest(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		if channel == self.bot.nick:
			channel = nick
		
		(command, suggestion) = splitnum(string)
		command = command.lower()
		
		if suggestion == '':
			output_lines = ['SUGEST SYNTAX: '+self.bot.prefix+'suggest <command> <suggestion>',
							"<command> is what about goshu the suggestion affects; for example: if suggesting a different "+self.bot.prefix+"who output for someone, <command> would be who",
							'<suggestion> is the suggestion you want to pass on']
			for i in range(0, len(output_lines)):
				if i > 0:
					output = ' ' * self.bot.indent
				else:
					output = ''
				
				output += output_lines[i]
				
				self.bot.irc.privmsg(server, nick, output)
			return
		
		output = server + ' - '
		output += event.source() + ' - '
		output += command
		output += '\n\t'
		output += suggestion
		output += '\n'
		
		command_escape = ''
		for character in command:
			if character in self.valid_characters:
				command_escape += character
			else:
				command_escape += '_'
		path = 'suggestions/'+command_escape
		outfile = open(path, 'a')
		outfile.write(output)
		outfile.close()
		
		self.bot.irc.privmsg(server, nick, 'Thanks for your suggestion')
