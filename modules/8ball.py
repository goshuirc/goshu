#!/usr/bin/env python3
"""
8ball.py - Goshubot 8ball Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
import random

class Ball(Module):
	
	name = "Ball"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'8ball' : [self.ask, 'ask a question, gain an answer', 0],
			},
		}
		
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
	
	def ask(self, question, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		if channel == self.bot.nick:
			channel = nick
		
		if question == '':
			output = '8BALL SYNTAX: '+self.bot.prefix+'8ball <question>'
			
			self.bot.irc.privmsg(server, nick, output)
			return
		
		response = self.responses[random.randint(0,len(self.responses)-1)]
		
		output = response+', '+event.source().split('!')[0]
		
		self.bot.irc.privmsg(server, channel, output)
