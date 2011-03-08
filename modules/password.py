#!/usr/bin/env python
"""
password.py - Goshubot Password Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from gbot.modules import Module

class Password(Module):
	
	name = "Password"
	
	def __init__(self):
		self.text_commands = {
			'privmsg' : {
				'change_password' : self.change_password
			},
			'pubmsg' : {
				'change_password' : self.change_password
			},
		}
		self.commands = {}
	
	def change_password(self, line, connection, event):
		if line == None and connection == None and event == None:
			text_commands_info = {
				'change_password' : [10, 10, 'change bot password'],
			}
			return (text_commands_info)
		
		elif self.gbot.level(event.source()) >= self.gbot.text_commands_info['change_password'][0]:
			try:
				(new_pass, repeat_pass) = line.split(' ')
			except:
				output = 'PASSWORD SYNTAX: '+self.gbot.prefix+'change_password <new password> <repeat new password>'
				
				connection.privmsg(event.source().split('!')[0], output)
				return
		
			if new_pass != repeat_pass:
				output = 'PASSWORD: New Password and Repeat New Password are different'
				
				connection.privmsg(event.source().split('!')[0], output)
				return
			
			del self.gbot.password
			self.gbot.password = hashlib.sha512(new_pass)
			connection.privmsg(event.source().split('!')[0], 'PASSWORD: Password Updated')
		
		else:
			output = 'Unauthorised \'' + self.gbot.prefix + 'change_password\' '
			output += 'attempt from: ' + event.source()
			print output
