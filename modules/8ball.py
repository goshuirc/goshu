#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot	-	http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.girclib import escape
import random

class eightball(Module):
	name = 'eightball'
	
	def __init__(self):
		self.events = {
			'commands' : {
				'8ball' : [self.ask, '<question> --- ask a question, gain an answer', 0],
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
	
	def ask(self, event, command):
		response = self.responses[random.randint(0,len(self.responses)-1)]
		response += ', ' + escape(event.source.split('!')[0])
		
		self.bot.irc.servers[event.server].privmsg(event.from_to, response)