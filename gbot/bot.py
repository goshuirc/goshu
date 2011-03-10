#!/usr/bin/env python
"""
bot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

import irc

class Bot:
	""" Brings everything together."""
	
	def __init__(self, prefix='.', indent=3, module_path='modules'):
		self.irc = irc.IRC()
		
		self.irc.connect('127', '127.0.0.1', 6667, 'goshubot')
		self.irc.privmsg('127', 'Danneh_', 'lolk')
		
		self.irc.process_forever()
