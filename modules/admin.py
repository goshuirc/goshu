#!/usr/bin/env python
"""
admin.py - Goshubot Administration Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import random
import hashlib
from gbot.modules import Module

class Admin(Module):
	
	name = "Admin"
	
	def __init__(self):
		self.run = random.randint(1, 10000)
		self.text_commands = {
			'privmsg' : { 
				'op' : self.op,
			},
		}
		self.commands = {}
	
	def op(self, line, connection, event):
		if line == None or connection == None or event == None:
			return ("OP", "OP-related functions", self.run)
