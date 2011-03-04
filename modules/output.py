#!/usr/bin/env python
"""
output.py - Goshubot Output Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
from time import strftime, localtime
from colorama import init
init() #colorama
from colorama import Fore, Back, Style
import textwrap
from gbot.modules import Module

class Output(Module):
	
	name = "Output"
	
	def __init__(self):
		self.text_commands = {}
		self.commands = {
			'all_events' : [ self.log ],
		}
		self.log = True
		self.out = True
		self.welcomed = False
	
	def log(self, connection, event):
		seperator = Fore.BLUE+'-'+Fore.RESET
		
		if event.eventtype() == 'all_raw_messages':
			return
		
		elif event.eventtype() in [ 'privnotice', 'motdstart', 'motd',
		                            'endofmotd', 'welcome', 'yourhost',
		                            'created', 'luserclient', 'luserme',
		                            'n_local', 'n_global', 'luserconns' ]:
		    
			if event.eventtype() == 'welcome':
				self.welcomed = True
		    
			if event.target() == 'AUTH' or self.welcomed == False:
				nick = Fore.GREEN+event.source()+Fore.RESET
			elif self.gbot.server.get_server_name() == event.source():
				nick = seperator+'!'+seperator
			else:
				nick = seperator+Fore.GREEN+event.source().split('!')[0]+Fore.RESET+Style.DIM+'('+Fore.GREEN+event.source().split('!')[1]+Fore.RESET+Style.DIM+')'+Style.RESET_ALL+seperator
			print strftime("%H:%M", localtime()), nick, event.arguments()[0]
		
		elif event.eventtype() in [ 'myinfo', 'featurelist', 'luserop',
									'luserchannels' ]:
			line_out = ''
			for line in event.arguments():
				line_out += line+' '
			line_out = line_out[:-1]
			line_out = textwrap.fill(line_out, initial_indent='', subsequent_indent='          ')
			print strftime("%H:%M", localtime()), Fore.BLUE+'-'+Fore.RESET+'!'+Fore.BLUE+'-'+Fore.RESET, line_out
			
		elif event.eventtype() == 'pubmsg':
			print strftime("%H:%M", localtime()),'PUB: <'+event.source().split('!')[0]+'>',event.arguments()[0]
			
		elif event.eventtype() == 'privmsg':
			print strftime("%H:%M", localtime()),'PRI: <'+event.source().split('!')[0]+'>',event.arguments()[0]
		
		elif event.eventtype() == 'umode':
			print strftime("%H:%M", localtime()), seperator+'!'+seperator, 'Mode change', Style.DIM+'['+Style.RESET_ALL+event.arguments()[0]+Style.DIM+']'+Style.RESET_ALL, 'for user', event.target()
		
		elif event.eventtype() == 'mode':
			print strftime("%H:%M", localtime()),seperator+'!'+seperator, 'mode/'+Fore.CYAN+event.target()+Fore.RESET, Style.DIM+'['+Style.RESET_ALL+event.arguments()[0]+Style.DIM+']'+Style.RESET_ALL, 'by', event.source().split('!')[0]
			
		elif event.eventtype() == 'join':
			print strftime("%H:%M", localtime()),seperator+'!'+seperator, Style.BRIGHT+Fore.CYAN+event.source().split('!')[0]+Fore.RESET+Style.RESET_ALL, Style.DIM+'['+Style.RESET_ALL+Fore.CYAN+event.source().split('!')[1]+Fore.RESET+Style.DIM+']'+Style.RESET_ALL, 'has joined', event.target()
			print ''
		
		else:
			print "command: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments())
