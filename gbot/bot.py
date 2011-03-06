#!/usr/bin/env python
"""
bot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import os
import sys
import hashlib
from gbot.modules import ModuleLoader

class Bot(object):
	""" Handles Bot operations."""
	
	def __init__(self, server, password, prefix='.', indent=3, module_path='modules'):
		""" Sets up bot."""
		self.server = server
		
		self.prefix = prefix
		self.indent = indent
		
		self.module = None
		self.modules = {}
		self.text_commands_info = {} #detailed info about text commands
		self.text_commands = {
			'privmsg' : {},
			'pubmsg' : {},
		} #commands responding to <prefix><command> <arg>
		self.commands = {} #commands that respond to events
		
		self.password = hashlib.sha512(password)
		self.ops = {
			#'name/hostname' : <access level>,
		}
		self.load(module_path)
	
	def load(self, path):
		""" Loads modules."""
		loader = ModuleLoader(path)
		for module in loader:
			self.append(module)
	
	def append(self, module):
		""" Appends a module to the bot."""
		module.gbot = self
		self.modules[module.name] = module
		for event in module.text_commands:
			for alias in module.text_commands[event]:
				self.text_commands[event][alias] = module.text_commands[event][alias]
				module_commands_info = module.text_commands[event][alias](None, None, None)
				self.text_commands_info.update(module_commands_info)
		self.commands.update(module.commands)
	
	def handle(self, connection, event):
		""" Handle messages"""
		if event.eventtype() == 'privmsg' or event.eventtype() == 'pubmsg':
			if event.arguments()[0].split(self.prefix)[0] == '': #command for us
				command = event.arguments()[0].split(self.prefix)[1].split(' ')[0]
				
				arg_offset = 0
				arg_offset += len(self.prefix)
				arg_offset += len(command)
				try:
					event.arguments()[0].split(self.prefix)[1].split(' ')[1]
					arg_offset += 1
				except:
					pass
			
				try: arg = event.arguments()[0][arg_offset:].strip()
				except: arg = ''
			
				try:
					self.text_commands[event.eventtype()][command](arg, connection, event)
				except KeyError:
					print 'Bot handle: fail - command not found'
					print ' command:', command
					print ' arg:', arg
					print self.text_commands[event.eventtype()]
				except:
					print 'Bot handle: fail'
					print ' command:', command
					print ' arg:', arg
					self.text_commands[event.eventtype()][command](arg, connection, event)
		
		try:
			for command in self.commands[event.eventtype()]:
				command(connection, event)
		except:
			pass
		
		try:
			for command in self.commands['all_events']:
					command(connection, event)
		except:
			pass
	
	def level(self, user):
		try:
			return self.ops[user]
		except:
			return 0
	
	def is_password(self, password):
		if hashlib.sha512(password).hexdigest() == self.password.hexdigest():
			return True
		else:
			return False
	
	def quit(self, message):
		""" Quits, may accept a server/channel name later on, once it can join
		    multiple servers/channels."""
		self.server.disconnect(message)
		# TODO: exit bot
