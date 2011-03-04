#!/usr/bin/env python
"""
log.py - Goshubot Logging Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.modules import Module

class Log(Module):
	
	name = "Log"
	
	def __init__(self):
		self.text_commands = {}
		self.commands = {
			'all_events' : [ self.log ],
		}
	
	def log(self, connection, event):
		if event.eventtype() == 'pubmsg':
			print 'PUB: <'+event.source().split('!')[0]+'>',event.arguments()[0]
		elif event.eventtype() == 'privmsg':
			print 'PRI: <'+event.source().split('!')[0]+'>',event.arguments()[0]
		elif event.eventtype() == 'privnotice':
			print event.arguments()[0]
		else:
			print "command: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments())
