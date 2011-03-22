#!/usr/bin/env python
"""
log.py - Goshubot logging Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module

class Log(Module):
	
	name = "Log"
	
	def __init__(self):
		self.events = {
			'in' : {
				'all_events' : self.log_in,
			},
			'out' : {
				'all_events' : self.log_out,
			},
		}
	
	def log_in(self, connection, event):
		#print 'log_in:', connection, event
		pass
	
	def log_out(self, connection, event):
		#print 'log_out:', connection, event
		pass
