#!/usr/bin/env python
"""
log.py - Goshubot logging Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
from time import strftime, localtime
from colorama import init
init() #colorama
from colorama import Fore, Back, Style
import textwrap

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
		#print '<<'
		server = self.bot.irc.server_nick(connection)
		try:
			nick = event.source().split('!')[0]
			channel = event.target().split('!')[0]
			if channel == self.bot.nick:
				channel = nick
		except:
			nick = event.source()
			channel = nick
		seperator = Fore.BLUE+'-'+Fore.RESET
		server_print = Fore.GREEN+'-'+Fore.RESET+server+Fore.GREEN+'-'+Fore.RESET
		server_ident_print = seperator+'!'+seperator
		output = strftime("%H:%M", localtime())+' '+server_print+' '
		#print event.eventtype()
		
		
		if event.eventtype() == 'all_raw_messages':
			pass
		
		elif event.eventtype() == 'privnotice':
			#if event.source() == connection.get_server_name():
			output += Fore.GREEN+event.source()+Fore.RESET+' '
			for message in event.arguments():
				output += message+' '
			print output
		
		elif event.eventtype() in ['welcome', 'yourhost', 'created', 'myinfo',
								   'featurelist', 'luserclient', 'luserop',
								   'luserchannels', 'luserme', 'n_local',
								   'n_global', 'luserconns', 'motdstart',
								   'motd', 'endofmotd', ]:
			output += server_ident_print+' '
			for message in event.arguments():
				output += message+' '
			print output
		
		elif event.eventtype() in ['nicknameinuse', ]:
			output += server_ident_print+' '
			try:
				output += event.arguments()[1]
			except:
				output += event.arguments()
			print output
		
		elif event.eventtype() in ['invite', ]:
			output += server_ident_print+' '
			output += nick
			output += ' invites you to '
			output += event.arguments()[0]
			print output
		
		elif event.eventtype() in ['join', ]:
			output += server_ident_print+' '
			output += 'Joined '
			output += event.target()
			print output
		
		elif event.eventtype() in ['umode', ]:
			output += server_ident_print+' '
			output += 'Mode change '
			output += Style.DIM+'['+Style.RESET_ALL
			output += event.arguments()[0]
			output += Style.DIM+']'+Style.RESET_ALL
			output += ' for user '
			output += event.target()
			print output
		
		elif event.eventtype() in ['pubmsg', ]:
			output += seperator
			output += event.target()
			output += seperator
			output += Style.DIM+' <'+Style.RESET_ALL
			output += nick
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()[0]
			print output
		
		elif event.eventtype() in ['privmsg', ]:
			output += server_ident_print
			output += Style.DIM+' <'+Style.RESET_ALL
			output += nick
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()[0]
			print output
		
		else:
			print "log_in: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments())
		#print '>>'
	
	def log_out(self, connection, event):
		nick = event.source()
		target = event.target()
		
		if event.eventtype() == 'all_raw_messages':
			pass
		
		elif event.eventtype() in ['pubmsg', ]:
			output += seperator
			output += event.target()
			output += seperator
			output += Style.DIM+' <'+Style.RESET_ALL
			output += nick
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()[0]
			print output
		
		elif event.eventtype() in ['privmsg', ]:
			output += seperator
			output += event.target()
			output += seperator
			output += Style.DIM+' <'+Style.RESET_ALL
			output += nick
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()[0]
			print output
		
		else:
			print "log_out: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments())
