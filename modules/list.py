#!/usr/bin/env python
"""
list.py - Goshubot listing Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module

class List(Module):
	
	name = "List"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'list' : [self.list_commands, 'lists avaliable commands', 0],
			},
		}
	
	def list_commands(self, line):
		for command in self.bot.modules.events['commands']:
			print command
