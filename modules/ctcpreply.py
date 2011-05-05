#!/usr/bin/env python
"""
ctcpreply.py - Goshubot ctcpreply Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from time import strftime, localtime, gmtime
from gbot.modules import Module
from gbot.helper import splitnum
from gbot.libs.irclib import nm_to_n

class Ctcpreply(Module):
	
	name = "ctcp_reply"
	
	def __init__(self):
		self.events = {
			'in' : {
				'ctcp' : self.ctcp_reply
			},
			#'out' : {},
			#'commands' : {},
		}
	
	def ctcp_reply(self, connection, event):
		server = self.bot.irc.server_nick(connection)
		
		if event.arguments()[0] == 'VERSION':
			self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'VERSION Goshubot:beta:None')
		
		elif event.arguments()[0] == 'SOURCE':
			self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'SOURCE github.com/Danneh/Goshubot')
		
		elif event.arguments()[0] == 'USERINFO':
			#self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'USERINFO :Please don\'t kline me, I\'ll play nice!')
			pass
		
		elif event.arguments()[0] == 'CLIENTINFO':
			self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'CLIENTINFO ') # to be continued
		
		elif event.arguments()[0] == 'ERRMSG':
			#self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'ERRMSG '+event.arguments()[1]+':ERRMSG echo, no error has occured') #could be bad, errmsg-storm, anyone?
			pass
		
		elif event.arguments()[0] == 'TIME':
			self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'TIME '+strftime("%a %b %d, %H:%M:%S %Y", localtime()))
		
		elif event.arguments()[0] == 'PING':
			if len(event.arguments()) > 1:
				self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), "PING " + event.arguments()[1])
