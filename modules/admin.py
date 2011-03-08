#!/usr/bin/env python
"""
admin.py - Goshubot Administration Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.helper import splitnum
from gbot.modules import Module

class Admin(Module):
	
	name = "Admin"
	
	def __init__(self):
		self.text_commands = {
			'privmsg' : { 
				'op' : self.op,
			},
			'pubmsg' : { 
				'op' : self.op,
			},
		}
		self.commands = {
			'endofwhois' : [self.finish_waiting],
			'nick' : [self.update_nick],
		}
		self.waiting = {
			
		}
	
	def op(self, line, connection, event):
		if line == None and connection == None and event == None:
			text_commands_info = {
				"op owner" : [0, 0, 'make yourself a bot owner'],
			}
			return (text_commands_info)
			
		try:
			(command, line) = splitnum(line)
		except:
			output = 'OP: Command Failed'
			
			connection.privmsg(event.source().split('!')[0], output)
			return
		
		if command == 'owner':
			password = line
			
			if self.gbot.is_password(password):
				nick = event.source().split('!')[0]
				print self.waiting
				try:
					self.waiting[nick].append('owner')
				except:
					self.waiting[nick] = {
						'nickhost' : event.source(),
						'privs' : ['owner'],
					}
				print self.waiting
				self.gbot.server.whois([nick])
	
	def finish_waiting(self, connection, event):
		""" Finishes waiting requests."""
		nick = event.arguments()[0]
		
		try:
			commands = self.waiting[nick]['privs']
		except:
			return # user isn't waiting for anything 
		
		if 'owner' in commands:
			if event.eventtype() == 'endofwhois':
				self.gbot.ops[self.waiting[nick]['nickhost']] = 10
				output = 'You have been made a bot owner, congrats'
				connection.privmsg(nick, output)
	
	def update_nick(self, connection, event):
		""" Updates op list in relation to nick changes."""
		nick = event.source().split('!')[0]
		host = event.source().split('!')[1]
		nick_new = event.target()
		
		try:
			priv_level = self.gbot.op[nick]
			del self.gbot.op[nick]
			
			# check if new nick is +r as well
		except:
			pass
		
		try:
			priv_level = self.gbot.op[nick+'!'+host]
			del self.gbot.op[nick+'!'+host]
			nick_new += '!'+host
		except:
			pass
		
		try:
			self.gbot.op[nick_new] = priv_level
			output = 'Bot owner updated from '+nick
			connection.privmsg(nick_new, output)
		except:
			pass
