#!/usr/bin/env python
"""
ctcpreply.py - Goshubot ctcpreply Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
from gbot.helper import splitnum
from gbot.libs.irclib3 import nm_to_n

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
			self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), 'VERSION goshubot')
		
		elif event.arguments()[0] == 'PING':
			if len(event.arguments()) > 1:
				self.bot.irc.ctcp_reply(server, nm_to_n(event.source()), "PING " + event.arguments()[1])
