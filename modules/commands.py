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
				'ignore' : [self.ignore, 'ignore', 10],
				'unignore' : [self.unignore, 'unignore', 10],
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
	
	def ignore(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		nick = event.source().split('!')[0]
		(password, nickhost) = splitnum(string)
		pass_hash = self.bot.encrypt(password.encode('utf-8'))
		
		if self.bot.pass_hash == pass_hash:
			nickhost = nickhost.split('!')[0]
			self.bot.irc._nick_ignore_list.append(nickhost)
			self.bot.irc.privmsg(server, nick, nickhost+' has been ignored')
	
	def unignore(self, string, connection, event):
		server = self.bot.irc.server_nick(connection)
		nick = event.source().split('!')[0]
		(password, nickhost) = splitnum(string)
		pass_hash = self.bot.encrypt(password.encode('utf-8'))
		
		if self.bot.pass_hash == pass_hash:
			nickhost = nickhost.split('!')[0]
			print('lol')
			for i in range(len(self.bot.irc._nick_ignore_list)):
				if self.bot.irc._nick_ignore_list[i] == nickhost:
					del self.bot.irc._nick_ignore_list[i]
			self.bot.irc.privmsg(server, nick, nickhost+' has been unignored')
