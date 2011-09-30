#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot	-	http://danneh.net/goshu

from gbot.modules import Module

class commands(Module):
	name = 'commands'
	
	def __init__(self):
		self.events = {
			'commands' : {
				'msg' : [self.msg, '<user> <message> --- send a /msg', 3],
				'me' : [self.me, '<user> <message> --- send a /me', 3],
			},
		}
	
	def msg(self, event, command):
		split_arguments = command.arguments.split(' ', 1)
		if len(split_arguments) < 2:
			split_arguments.append(' ')
		
		(msg_target, msg_msg) = split_arguments
		
		self.bot.irc.servers[event.server].privmsg(msg_target, msg_msg)
	
	def me(self, event, command):
		split_arguments = command.arguments.split(' ', 1)
		if len(split_arguments) < 2:
			split_arguments.append(' ')
		
		(msg_target, msg_msg) = split_arguments
		
		self.bot.irc.servers[event.server].action(msg_target, msg_msg)