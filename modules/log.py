#!/usr/bin/env python3
"""
log.py - Goshubot logging Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
from gbot.helper import splitnum
from time import strftime, localtime, gmtime
from colorama import init
init() #colorama
from colorama import Fore, Back, Style
import textwrap
import random
import os
import sys
import string

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
		
		self.Fore = {
			'BLACK' : '/{Fore.BLACK}',
			'RED' : '/{Fore.RED}',
			'GREEN' : '/{Fore.GREEN}',
			'YELLOW' : '/{Fore.YELLOW}',
			'BLUE' : '/{Fore.BLUE}',
			'MAGENTA' : '/{Fore.MAGENTA}',
			'CYAN' : '/{Fore.CYAN}',
			'WHITE' : '/{Fore.WHITE}',
			'RESET' : '/{Fore.RESET}',
		}
		self.Back = {
			'BLACK' : '/{Fore.BLACK}',
			'RED' : '/{Fore.RED}',
			'GREEN' : '/{Fore.GREEN}',
			'YELLOW' : '/{Fore.YELLOW}',
			'BLUE' : '/{Fore.BLUE}',
			'MAGENTA' : '/{Fore.MAGENTA}',
			'CYAN' : '/{Fore.CYAN}',
			'WHITE' : '/{Fore.WHITE}',
			'RESET' : '/{Fore.RESET}',
		}
		self.Style = {
			'DIM' : '/{Style.DIM}',
			'NORMAL' : '/{Style.NORMAL}',
			'BRIGHT' : '/{Style.BRIGHT}',
			'RESET_ALL' : '/{Style.RESET_ALL}',
		}
		
		self.nick_colors = {
			#'nick' : 'color'
		}
		self.textwrapper = textwrap.TextWrapper()
		random.seed()
	
	def log_in(self, connection, event):
		""" Logs incoming events."""
		try:
			nick = self.color_string_escape(event.source().split('!')[0])
			host = self.color_string_escape(event.source().split('!')[1])
		except:
			nick = self.color_string_escape(event.source())
			host = ''
		
		try:
			channel = self.color_string_escape(event.target().split('!')[0])
		except:
			channel = self.color_string_escape(event.target())
		
		if self.color_string_unescape(channel) == self.bot.nick:
			channel = nick
		server = self.bot.irc.server_nick(connection)
		
		event_type = event.eventtype()
		event_arguments = []
		for argument in event.arguments():
			event_arguments.append(self.color_string_escape(argument))
		event_target = self.color_string_escape(event.target())
		
		sep_blue = self.Fore['BLUE']+'-'+self.Fore['RESET']
		sep_green = self.Fore['GREEN']+'-'+self.Fore['RESET']
		ident_server = sep_blue+'!'+sep_blue+' '
		
		
		output = ''
		output += self.Style['DIM']
		output += strftime("%H:%M", localtime())
		output += self.Style['RESET_ALL']
		output += ' '+sep_green+server+sep_green+' '
		
		indent =  self.printable_len(output)
		
		if event_type in ['all_raw_messages', 'ping', ]:
			return
		
		elif event_type in ['privnotice', '439', ]:
			output += self.Fore['GREEN']
			output += nick
			output += self.Fore['RESET']+' '
			for message in event_arguments:
				output += message+' '
		
		elif event_type in ['welcome', 'yourhost', 'created', 'myinfo',
							'featurelist', 'luserclient', 'luserop',
							'luserchannels', 'luserme', 'n_local',
							'n_global', 'luserconns', 'luserunknown',
							'motdstart', 'motd', 'endofmotd', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			for message in event_arguments:
				output += message+' '
		
		elif event_type in ['umode', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += 'Mode change '
			output += self.Style['DIM']+'['+self.Style['RESET_ALL']
			output += event_arguments[0]
			output += self.Style['DIM']+']'+self.Style['RESET_ALL']
			output += ' for user '
			output += self.Style['BRIGHT']
			output += event_target
		
		elif event_type in ['mode', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += 'mode/'
			output += self.Style['DIM']+self.Fore['CYAN']
			output += event_target
			output += self.Fore['RESET']
			output += ' ['
			output += self.Style['RESET_ALL']
			
			for arg in event_arguments:
				output += arg
				output += ' '
			output = output[:-1]
			
			output += self.Style['DIM']
			output += '] '
			output += self.Style['RESET_ALL']
			output += 'by user '
			output += self.Style['BRIGHT']
			output += nick
		
		elif event_type in ['nicknameinuse', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			try:
				output += event_arguments[1]
				output += ' '
				output += self.Style['DIM']+'['+self.Style['RESET_ALL']
				output += self.Style['BRIGHT']+event_arguments[0]
				output += self.Style['DIM']+']'+self.Style['RESET_ALL']
			except:
				output += event_arguments
		
		elif event_type in ['invite', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += self.Style['BRIGHT']
			output += nick
			output += self.Style['RESET_ALL']
			output += ' invites you to '
			output += self.Style['BRIGHT']
			output += event_arguments[0]
			output += self.Style['RESET_ALL']
		
		elif event_type in ['join', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += self.Style['BRIGHT']+self.Fore['CYAN']
			output += nick
			output += self.Fore['RESET']+self.Style['RESET_ALL']
			output += ' '
			output += self.Style['DIM']+'['
			output += self.Fore['CYAN']
			output += self.color_string_escape(event.source().split('!')[1])
			output += self.Fore['RESET']
			output += ']'+self.Style['RESET_ALL']
			output += ' has joined '
			output += self.Style['BRIGHT']
			output += event_target
			output += self.Style['RESET_ALL']
		
		elif event_type in ['currenttopic', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += 'Topic for '
			output += self.Style['DIM']+self.Fore['CYAN']
			output += event_arguments[0]
			output += self.Fore['RESET']+self.Style['RESET_ALL']
			output += ': '
			output += event_arguments[1]
		
		elif event_type in ['topicinfo', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += 'Topic set by '
			
			output += self.Style['BRIGHT']
			output += event_arguments[1].split('!')[0]
			output += self.Style['RESET_ALL']
			output += self.Style['DIM']
			output += ' ['
			output += self.Style['RESET_ALL']
			output += event_arguments[1].split('!')[1]
			output += self.Style['DIM']
			output += '] '
			output += self.Style['RESET_ALL']
			
			output += 'on'
			
			output += self.Style['DIM']
			output += ' ['
			output += self.Style['RESET_ALL']
			output += strftime("%a %b %d, %H:%M:%S %Y", gmtime(int(event_arguments[2])))
			output += self.Style['DIM']
			output += '] '
			output += self.Style['RESET_ALL']
		
		elif event_type in ['paert', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += self.Fore['CYAN']
			output += nick
			output += self.Fore['RESET']
			output += ' '
			output += self.Style['DIM']+'['+self.Style['RESET_ALL']
			output += host
			output += self.Style['DIM']+']'+self.Style['RESET_ALL']
			output += ' has left '
			output += self.Style['BRIGHT']
			output += channel
			output += self.Style['RESET_ALL']
		
		elif event_type in ['quait', ]:
			output += server_ident_print+' '
			#output += Fore.CYAN+nick+Fore.RESET
			output += ' '
			output += Style.DIM+'['+Style.RESET_ALL
			#output += event.source().split('!')[1]
			output += Style.DIM+']'+Style.RESET_ALL
			output += ' has quit '
			output += Style.DIM+'['+Style.RESET_ALL
			#output += event.arguments()[0]
			output += Style.DIM+']'+Style.RESET_ALL
		
		elif event_type in ['pubmsg', ]:
			output += sep_blue
			output += channel
			output += sep_blue
			output += self.Style['DIM']+' <'+self.Style['RESET_ALL']
			output += self.nick_symbol(nick)
			output += self.nick_color(nick)
			output += nick
			output += self.Fore['RESET']
			output += self.Style['DIM']+'> '+self.Style['RESET_ALL']
			indent = self.printable_len(output)
			output += event_arguments[0]
		
		elif event_type in ['privmsg', ]:
			output += sep_blue
			output += nick
			output += sep_blue
			output += self.Style['DIM']+' <'+self.Style['RESET_ALL']
			output += self.nick_color(nick)
			output += nick
			output += self.Fore['RESET']
			output += self.Style['DIM']+'> '+self.Style['RESET_ALL']
			indent = self.printable_len(output)
			output += event_arguments[0]
		
		elif event_type in ['nick', ]:
			output += ident_server
			indent = self.printable_len(output)
			
			output += self.Fore['CYAN']
			output += nick
			output += self.Fore['RESET']
			output += ' is now known as '
			output += self.Style['BRIGHT']+self.Fore['CYAN']
			output += channel
			output += self.Fore['RESET_ALL']+self.Style['RESET_ALL']
		
		else:
			output += "log_in: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments())
		
		self.log(output, indent)
	
	def log_out(self, connection, event):
		""" Logs outgoing events."""
		try:
			nick = self.color_string_escape(event.source().split('!')[0])
			host = self.color_string_escape(event.source().split('!')[1])
		except:
			nick = self.color_string_escape(event.source())
			host = ''
		
		try:
			channel = self.color_string_escape(event.target().split('!')[0])
		except:
			channel = self.color_string_escape(event.target())
		
		if self.color_string_unescape(channel) == self.bot.nick:
			channel = nick
		server = self.bot.irc.server_nick(connection)
		
		event_type = event.eventtype()
		event_arguments = []
		for argument in event.arguments():
			event_arguments.append(self.color_string_escape(argument))
		event_target = self.color_string_escape(event.target())
		
		sep_blue = self.Fore['BLUE']+'-'+self.Fore['RESET']
		sep_green = self.Fore['GREEN']+'-'+self.Fore['RESET']
		ident_server = sep_blue+'!'+sep_blue+' '
		
		
		output = ''
		output += self.Style['DIM']
		output += strftime("%H:%M", localtime())
		output += self.Style['RESET_ALL']
		output += ' '+sep_green+server+sep_green+' '
		
		indent = self.printable_len(output)
		
		if event_type in ['all_raw_messages', 'ping', ]:
			pass
		
		elif event_type in ['action', ]:
			output += sep_blue
			output += channel
			output += sep_blue
			output += self.Style['BRIGHT']
			output += ' * '+nick
			output += self.Style['RESET_ALL']
			output += ' '
			indent = self.printable_len(output)
			output += event_arguments[0]
		
		elif event_type in ['privmsg', ]:
			output += sep_blue
			output += channel
			output += sep_blue
			output += self.Style['DIM']+' <'+self.Style['RESET_ALL']
			output += self.nick_symbol(nick)
			output += self.Style['BRIGHT']
			output += nick
			output += self.Style['RESET_ALL']
			output += self.Fore['RESET']
			output += self.Style['DIM']+'> '+self.Style['RESET_ALL']
			indent = self.printable_len(output)
			output += event_arguments[0]
		
		else:
			output += "log_in: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments())
			
		
		self.log(output, indent)
		
		if False:
			if event.eventtype() == 'all_raw_messages':
				pass
		
			elif event.eventtype() in ['acnbtion', ]:
				output += seperator
				output += event.target()
				output += seperator
				output += self.nick_symbol(nick)
				output += self.nick_color(nick)[0]
				output += nick+' '
				output += event.arguments()
		
			elif event.eventtype() in ['privmsg', ]:
				output += seperator
				output += event.target()
				output += seperator
				output += Style.DIM+' <'+Style.RESET_ALL
				output += self.nick_symbol(nick)
				output += self.nick_color(nick)[0]
				output += nick
				output += Fore.RESET
				output += Style.DIM+'> '+Style.RESET_ALL
				output += event.arguments()
		
			else:
				self.log("log_out: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments()))
	
	
	def log(self, string, indent=0):
		""" print/log the given string, with a hanging indent of given spaces."""
		print(self.color_string_unescape(self.wrap(string, indent)))
	
	
	def printable_len(self, in_string):
		""" Gives how many printable characters long the string is."""
		printable = 0
		running = True
		while running:
			if in_string[0] == '/' and in_string[1] == '{':
				(temp_first, temp_last) = splitnum(in_string, split_char='}')
				in_string = temp_last
			elif in_string[0] == '/' and in_string[1] == '/':
				printable += 1
				in_string = in_string[2:]
			elif in_string[0] in string.printable: # change to work with unicode
				printable += 1
				in_string = in_string[1:]
			if len(in_string) < 1:
				running = False
		return printable
	
	
	def color_irc_parse(self, in_string):
		""" Parse the given string and turn irc color codes into our color
			codes."""
		return in_string
	
	def color_string_escape(self, in_string=None):
		""" Escapes an irc string, so it'll work properly with the color
			functions."""
		if in_string:
			in_string = in_string.replace('/', '//')
			in_string = self.color_irc_parse(in_string)
		else:
			in_string = ''
		return in_string
	
	def color_string_unescape(self, in_string=None):
		""" Replace color sequences with the proper codes and text for output."""
		if in_string:
			for code in self.Fore:
				in_string = in_string.replace(self.Fore[code], eval('Fore.'+code))
			for code in self.Back:
				in_string = in_string.replace(self.Back[code], eval('Back.'+code))
			for code in self.Style:
				in_string = in_string.replace(self.Style[code], eval('Style.'+code))
			in_string = in_string.replace('//', '/')
		else:
			in_string = ''
		return in_string
	
	def wrap(self, in_string, indent):
		rows, columns = os.popen('stty size', 'r').read().split()
		output = ''
		running = True
		i = 1
		line = 0
		while running:
			char = in_string[0]
			
			if char == '/' and in_string[1] == '{':
				(temp_first, temp_last) = splitnum(in_string, split_char='}')
				output += temp_first+'}'
				in_string = temp_last
			elif char == '/' and in_string[1] == '/':
				output += '//'
				i += 1
				in_string = in_string[2:]
			elif char in string.printable:
				output += char
				i += 1
				in_string = in_string[1:]
			else:
				output += char
				in_string = in_string[1:]
			
			if int(i) > int(columns):
				output += ' '*int(indent)
				i = 1
				if line == 0:
					columns = int(columns) - int(indent)
				line += 1
			if len(in_string) < 1:
				running = False
		
		return output
	
	
	def nick_symbol(self, nick):
		""" Returns the given nick's symbol, _/+/%/@/~/etc."""
		return ' '
	
	def nick_color(self, nick):
		""" Returns the nick's color, and generates a new one otherwise."""
		if nick == self.bot.nick:
			return ''
		
		try:
			color = self.nick_colors[nick]
		except:
			color = 'RESET'
			while color in ['BLACK', 'WHITE', 'RESET', ]:
				color_num = random.randint(1, len(list(self.Fore.keys()))) - 1
				color = list(self.Fore.keys())[color_num]
			self.nick_colors[nick] = color
		nick_color = self.Fore[color]
		return nick_color












	def log_in_really(self, connection, event):
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
		output = Style.DIM+strftime("%H:%M", localtime())+Style.RESET_ALL
		output += ' '+server_print+' '
		#print event.eventtype()
		indent = 0
		
		
		if event.eventtype() in ['all_raw_messages', 'ping', ]:
			pass
		
		elif event.eventtype() in ['privnotice', '439', ]:
			#if event.source() == connection.get_server_name():
			output += Fore.GREEN+event.source()+Fore.RESET+' '
			for message in event.arguments():
				output += message+' '
			self.log(output, indent)
		
		elif event.eventtype() in ['welcome', 'yourhost', 'created', 'myinfo',
								   'featurelist', 'luserclient', 'luserop',
								   'luserchannels', 'luserme', 'n_local',
								   'n_global', 'luserconns', 'motdstart',
								   'motd', 'endofmotd', ]:
			output += server_ident_print+' '
			for message in event.arguments():
				output += message+' '
			self.log(output, indent)
		
		elif event.eventtype() in ['nicknameinuse', ]:
			output += server_ident_print+' '
			try:
				output += event.arguments()[1]
			except:
				output += event.arguments()
			self.log(output, indent)
		
		elif event.eventtype() in ['invite', ]:
			output += server_ident_print+' '
			output += nick
			output += ' invites you to '
			output += Style.DIM+Fore.CYAN+event.arguments()[0]+Fore.RESET+Style.RESET_ALL
			self.log(output, indent)
		
		elif event.eventtype() in ['join', ]:
			output += server_ident_print+' '
			output += Style.BRIGHT+Fore.CYAN+nick+Fore.RESET+Style.RESET_ALL
			output += ' '
			output += Style.DIM+'['
			output += Fore.CYAN
			output += event.source().split('!')[1]
			output += Fore.RESET
			output += ']'+Style.RESET_ALL
			output += ' has joined '
			output += Style.BRIGHT+event.target()+Style.RESET_ALL
			self.log(output, indent)
		
		elif event.eventtype() in ['part', ]:
			output += server_ident_print+' '
			output += Fore.CYAN+nick+Fore.RESET
			output += ' '
			output += Style.DIM+'['+Style.RESET_ALL
			output += event.source().split('!')[1]
			output += Style.DIM+']'+Style.RESET_ALL
			output += ' has left '
			output += Style.BRIGHT+event.target()+Style.RESET_ALL
			self.log(output, indent)
		
		elif event.eventtype() in ['aquit', ]:
			print('QUIT')
			output += server_ident_print+' '
			#output += Fore.CYAN+nick+Fore.RESET
			output += ' '
			output += Style.DIM+'['+Style.RESET_ALL
			#output += event.source().split('!')[1]
			output += Style.DIM+']'+Style.RESET_ALL
			output += ' has quit '
			output += Style.DIM+'['+Style.RESET_ALL
			#output += event.arguments()[0]
			output += Style.DIM+']'+Style.RESET_ALL
			#print(output)
			self.log(output, indent)
		
		elif event.eventtype() in ['currenttopic', ]:
			output += server_ident_print+' '
			output += 'Topic for '
			output += Style.DIM+Fore.CYAN+event.arguments()[0]+Fore.RESET+Style.RESET_ALL
			output += ': '
			topic = self.colors_parse(event.arguments()[1])
			output += topic
			self.log(output, indent)
		
		elif event.eventtype() in ['topicinfo', ]:
			output += server_ident_print+' '
			output += 'Topic'# for '
			#output += Style.DIM+Fore.CYAN+event.arguments()[0]+Fore.RESET+Style.RESET_ALL
			output += ' set by '
			output += Style.BRIGHT+event.arguments()[1].split('!')[0]+Style.RESET_ALL
			output += Style.DIM+' ['+Style.RESET_ALL
			output += event.arguments()[1].split('!')[1]
			output += Style.DIM+'] '+Style.RESET_ALL
			output += 'at'
			output += Style.DIM+' ['+Style.RESET_ALL
			output += strftime("%a %b %d, %H:%M:%S %Y", gmtime(int(event.arguments()[2])))
			output += Style.DIM+'] '+Style.RESET_ALL
			self.log(output, indent)
		
		elif event.eventtype() in ['nick', ]:
			output += server_ident_print+' '
			output += Style.DIM+Fore.CYAN+nick+Fore.RESET+Style.RESET_ALL
			output += ' is now known as '
			output += Style.BRIGHT+Fore.CYAN+event.target()+Fore.RESET+Style.RESET_ALL
			self.log(output, indent)
			self.nick_colors[event.target()] = self.nick_colors[nick]
			del self.nick_colors[nick]
		
		elif event.eventtype() in ['umode', ]:
			output += server_ident_print+' '
			output += 'Mode change '
			output += Style.DIM+'['+Style.RESET_ALL
			output += event.arguments()[0]
			output += Style.DIM+']'+Style.RESET_ALL
			output += ' for user '
			output += event.target()
			self.log(output, indent)
		
		elif event.eventtype() in ['pubmsg', ]:
			indent = 60
			output += seperator
			output += event.target()
			output += seperator
			output += Style.DIM+' <'+Style.RESET_ALL
			output += self.nick_symbol(nick)
			output += self.nick_color(nick)[0]
			output += nick
			output += Fore.RESET
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()[0]
			self.log(output, indent)
		
		elif event.eventtype() in ['privmsg', ]:
			output += seperator
			output += nick
			output += seperator
			output += Style.DIM+' <'+Style.RESET_ALL
			output += self.nick_color(nick)[0]
			output += nick
			output += Fore.RESET
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()[0]
			self.log(output, indent)
		
		elif event.eventtype() in ['action', ]:
			output += seperator
			if event.target() == self.bot.nick:
				target = nick
			else:
				target = event.target()
			output += target
			output += seperator
			output += ' * '
			#output += self.nick_color(nick)[0]
			output += nick
			output += ' '+event.arguments()[0]
			self.log(output, indent)
		
		elif event.eventtype() in ['ctcp', ]:
			if event.arguments()[0] in ['ACTION', ]:
				pass
			else:
				self.log("log_in: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments()))
		
		else:
			self.log("log_in: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments()))
		#print '>>'
	
	def log_out_really(self, connection, event):
		seperator = Fore.BLUE+'-'+Fore.RESET
		server = self.bot.irc.server_nick(connection)
		server_print = Fore.GREEN+'-'+Fore.RESET+server+Fore.GREEN+'-'+Fore.RESET
		server_ident_print = seperator+'!'+seperator
		output = Style.DIM+strftime("%H:%M", localtime())+Style.RESET_ALL
		output += ' '+server_print+' '
		nick = event.source()
		target = event.target()
		
		if event.eventtype() == 'all_raw_messages':
			pass
		
		elif event.eventtype() in ['action', ]:
			output += seperator
			output += event.target()
			output += seperator
			output += self.nick_symbol(nick)
			output += self.nick_color(nick)[0]
			output += nick+' '
			output += event.arguments()
			self.log(output, indent)
		
		elif event.eventtype() in ['privmsg', ]:
			output += seperator
			output += event.target()
			output += seperator
			output += Style.DIM+' <'+Style.RESET_ALL
			output += self.nick_symbol(nick)
			output += self.nick_color(nick)[0]
			output += nick
			output += Fore.RESET
			output += Style.DIM+'> '+Style.RESET_ALL
			output += event.arguments()
			self.log(output, indent)
		
		else:
			self.log("log_out: %s, source: %s, target: %s, arguments: %s" % (event.eventtype(), event.source(), event.target(), event.arguments()))
		
	def nick_color_really(self, nick):
		""" Returns the nick's color, and generates a new one otherwise."""
		if nick == self.bot.nick:
			return ''
		try:
			color = self.nick_colors[nick]
		except:
			color_num = random.randint(1, len(self.colors)) - 1
			color = list(self.colors.keys())[color_num]
			self.nick_colors[nick] = color
		nick_color = self.colors[color]
		return nick_color
	
	def nick_symbol_really(self, nick):
		""" Returns the given nick's symbol, _/+/%/@/~/etc."""
		return ' '
	
	def log_really(self, string, indent):
		""" Print/log the given string."""
		#print string
		
		chars = ''
		for character in string:
			print(character)
			if self.isprintable(character):
				chars += character
		print(chars)
