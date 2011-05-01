#!/usr/bin/env python3
"""
invite.py - Goshubot invite Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module

class Invite(Module):
	
	name = "Invite"
	
	def __init__(self):
		self.events = {
			'in' : {
				'invite' : self.invite
			},
			#'out' : {},
			#'commands' : {},
		}
	
	def invite(self, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.arguments()[0]
		
		self.bot.irc.join(server, channel)
