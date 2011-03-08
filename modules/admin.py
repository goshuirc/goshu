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
				"op add" : [10, 10, 'add someone else as a bot op'],
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
				try:
					self.waiting[nick].append('owner')
				except:
					self.waiting[nick] = {
						'nickhost' : event.source(),
						'privs' : ['owner'],
					}
				self.gbot.server.whois([nick])
			
		elif command == 'add' and self.gbot.level(event.source(), 'op add') == True:
			try:
				(nick, level) = splitnum(line, 2)
				self.gbot.ops[nick] = level
				print nick, 'is now a bot op, level', level
			except:
				output = 'ADD: Command Failed'
				print output
	
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
		nickhost = event.source()
		nick_new = event.target()
		
		if self.gbot.level(event.source()) != 0:
			try: # registered nick
				priv_level = self.gbot.ops[nick]
				del self.gbot.ops[nick]
			except:# unregistered nick
				priv_level = self.gbot.ops[nickhost]
				del self.gbot.ops[nickhost]
				nick_new += '!'+host
			
			self.gbot.ops[nick_new] = priv_level
			
			if '!' in nick_new:
				nick_new = nick_new.split('!')[0]
			
			#output = 'Bot ops updated from '+nick
			#connection.privmsg(nick_new.split('!')[0], output)
