#!/usr/bin/env python
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
				'msg' : [self.msg, 'msg', 10],
				'me' : [self.me, 'me', 10],
			},
		}
	
	def quit(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		(password, message) = splitnum(string)
		password = self.bot.encrypt(password.encode('utf-8'))
		
		if self.bot.pass_hash == password:
			self.bot.irc.quit(server, message)
	
	def msg(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		(password, target, message) = splitnum(string, split_num=2)
		pass_hash = self.bot.encrypt(password.encode('utf-8'))
		
		if self.bot.pass_hash == pass_hash:
			self.bot.irc.privmsg(server, target, message)
	
	def me(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		(password, target, message) = splitnum(string, split_num=2)
		pass_hash = self.bot.encrypt(password.encode('utf-8'))
		
		if self.bot.pass_hash == pass_hash:
			self.bot.irc.action(server, target, message)
