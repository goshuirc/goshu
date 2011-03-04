#!/usr/bin/env python
"""
8ball.py - Goshubot 8ball Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

from gbot.modules import Module
import random

class Ball(Module):
	
	name = "Ball"
	
	def __init__(self):
		self.text_commands = {
			'privmsg' : { '8ball' : self.dice },
			'pubmsg' : { '8ball' : self.dice },
		}
		self.commands = {}
		random.seed()
		self.responses = [ "As I see it, yes", "It is certain", #good
						   "It is decidedly so", "Most likely",
						   "Outlook good", "Signs point to yes",
						   "Without a doubt", "Yes",
						   "Yes - definitely", "You may rely on it",
						   "Reply hazy, try again", "Ask again later", #meh
						   "Better not tell you now", "Cannot predict now",
						   "Concentrate and ask again",
						   "Don't count on it", "My reply is no", #bad
						   "My sources say no", "Outlook not so good",
						   "Very doubtful",
						 ]
	
	def dice(self, question, connection, event):
		if question == '':
			connection.privmsg(event.source().split('!')[0], '8BALL SYNTAX: .8ball <question>')
			return
		
		response = self.responses[random.randint(0,len(self.responses)-1)]
		
		connection.privmsg(event.target().split('!')[0], response+', '+event.source().split('!')[0])
