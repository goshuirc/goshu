#!/usr/bin/env python
"""
commands.py - Goshubot Commands Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.modules import Module

class Commands(Module):
	
	name = "Commands"
	
	def __init__(self):
		self.text_commands = {
			'privmsg' : { 
				'quit' : self.quit,
				'nick' : self.nick,
				'say' : self.say,
				'me' : self.me,
			},
		}
		self.commands = {}
	
	def quit(self, password, connection, event):
		if password == '':
			connection.privmsg(event.source().split('!')[0], 'QUIT SYNTAX: .quit <password>')
			return
		
		if self.gbot.is_password(password_pass):
			self.gbot.quit('QUIT issued by '+event.source().split('!')[0])
		
		else:
			connection.privmsg(event.source().split('!')[0], 'QUIT: Password Incorrect')
	
	def nick(self, line, connection, event):
		try:
			(password, nick) = line.split(' ')
		except:
			connection.privmsg(event.source().split('!')[0], 'NICK SYNTAX: .nick <password> <nick>')
			return
		
		if self.gbot.is_password(password):
			self.gbot.server.nick(nick)
		
		else:
			connection.privmsg(event.source().split('!')[0], 'NICK: Password Incorrect')
	
	def say(self, line, connection, event):
		try:
			line = line.split(' ')
			
			password = line[0]
			del line[0]
			
			target = line[0]
			del line[0]
			
			line_out = ''
			for line_part in line:
				line_out += line_part+' '
			line_out = line_out[:-1]
		except:
			connection.privmsg(event.source().split('!')[0], 'SAY SYNTAX: .say <password> <channel/nick> <line>')
			return
		
		if self.gbot.is_password(password):
			connection.privmsg(target, line_out)
		
		else:
			connection.privmsg(event.source().split('!')[0], 'SAY: Password Incorrect')
	
	def me(self, line, connection, event):
		try:
			line = line.split(' ')
			
			password = line[0]
			del line[0]
			
			target = line[0]
			del line[0]
			
			line_out = ''
			for line_part in line:
				line_out += line_part+' '
			line_out = line_out[:-1]
		except:
			connection.privmsg(event.source().split('!')[0], 'ME SYNTAX: .me <password> <channel/nick> <line>')
			return
		
		if self.gbot.is_password(password):
			connection.action(target, line_out)
		
		else:
			connection.privmsg(event.source().split('!')[0], 'ME: Password Incorrect')
