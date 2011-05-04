#!/usr/bin/env python3
"""
irc.py - Goshubot irclib Wrapper
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

import sys
from .helper import splitnum
from .libs import irclib3
#irclib3.DEBUG = True

class IRC(object):
	""" Acts as a wrapper for irclib. Highly convoluded wrapper, perhaps, but it
		is required so we can trap outgoing events."""
	
	def __init__(self, bot):
		self.bot = bot
		
		""" Events affect all servers."""
		self._irc = irclib3.IRC()
		self._servers = {
			#'example' : irclib.ServerConnection,
		}
		""" List of servers we are currently connected to."""
		self._irc.add_global_handler('all_events', self._handle_irclib)
		self._irc.add_global_handler('privmsg', self._handle_command)
		self._irc.add_global_handler('pubmsg', self._handle_command)
		
		self._nick_ignore_list = []
		self._host_ignore_list = []
	
	def connect(self, server_nickname, server, port, password=None, username=None,
				ircname=None, localaddress="", localport=0, sslsock=False, ipv6=False):
		""" Connects to the given server."""
		nickname = self.bot.nick
		current_server = self._irc.server()
		username = 'imouto-b'
		current_server.connect(server, port, nickname, password, username,
							ircname, localaddress, localport, sslsock, ipv6)
		self._servers[server_nickname] = current_server
		return current_server
	
	def connect_dict(self, dictionary):
		for server in dictionary:
			server_nickname = server
			server_address = dictionary[server]['address']
			server_ssl = dictionary[server]['ssl']
			server_port = dictionary[server]['port']
			self.connect(server_nickname, server_address, server_port, sslsock=server_ssl)
	
	def connection_prompt(self, dictionary=None):
		""" Prompt for server/channel connection details."""
		dictionary_out = {}
		more_servers = True
		print() #\newline
		
		if dictionary != None:
			dictionary_out.update(dictionary)
			for server in dictionary:
				print(server+':')
				print(' '+dictionary[server]['address']+':'+str(dictionary[server]['port']))
				if dictionary[server]['ssl']:
					ssl = 'Enabled'
				else:
					ssl = 'Disabled'
				print(' SSL', ssl)
				print('')
			
			more = ''
			while more != 'y' and more != 'n':
				more = input('Would you like to configure more connections? ')
			
			if more == 'y':
				more_servers = True
			else:
				more_servers = False
		else:
			more_servers = True
		
		while more_servers:
			server_nickname = input('Server Nickname: ')
			dictionary_out[server_nickname] = {}
			dictionary_out[server_nickname]['address'] = input('Server Address (irc.example.com): ')
			
			ssl = ''
			while ssl != 'y' and ssl != 'n':
				ssl = input('SSL? (y/n): ')
			
			if ssl == 'y':
				dictionary_out[server_nickname]['ssl'] = True
				assumed_port = 6697
			else:
				dictionary_out[server_nickname]['ssl'] = False
				assumed_port = 6667
			
			port = 'portnumberhere'
			while port.isdigit() == False and port != '':
				port = input('Port ['+str(assumed_port)+']: ')
			
			if port == '':
				dictionary_out[server_nickname]['port'] = assumed_port
			else:
				dictionary_out[server_nickname]['port'] = int(port)
			
			print(server_nickname, 'configured\n')
			
			more = 'test'
			while more[0] not in ['y', 'n']:
				more = input('Would you like to configure more connections? ')
			
			if more == 'y':
				more_servers = True
			else:
				more_servers = False
		
		return dictionary_out
		
	def server_nick(self, server_connection):
		""" Returns the server nickname of the given connection."""
		for server in self._servers:
			if self._servers[server] == server_connection:
				return server
		return None
	
	def _handle_irclib(self, connection, event):
		"""[Internal]"""
		handler_functions = self.modules.handlers('in', event.eventtype())
		#event = irclib3.Event(event.event_type, event.source, event.target, event.arguments)
		for handler in handler_functions:
			handler(connection, event)
	
	def _handle_command(self, connection, event):
		"""[Internal]"""
		if event.source().split('!')[0] in self._nick_ignore_list:
			return
		for host in self._host_ignore_list:
			if event.source().split('!')[1] == host:
				return
		
		(command, args) = (None, None)
		if event.arguments()[0].split(self.bot.prefix)[0] == '': #command for us
			(nothing, command) = splitnum(event.arguments()[0], split_char=self.bot.prefix)
			command = command.strip()
			
			(command, args) = splitnum(command)
			command = command.lower()
			
		handler_functions = self.modules.handlers('commands', command)
		for handler in handler_functions:
			try:
				handler[0](args, connection, event)
			except:
				print('===== Command Failed:', command)
				handler[0](args, connection, event)
	
	def _handle_out(self, event_type, server, target, arguments=None):
		source = self.bot.nick
		event = irclib3.Event(event_type, source, target, arguments)
		
		handler_functions = self.modules.handlers('out', event_type)
		for handler in handler_functions:
			handler(self._servers[server], event)
	
	
	def privmsg(self, server, target, message):
		""" Send a private message to target, on given server."""
		try: #overload target, so user can use event.source() directly
			target = target.split('!')[0]
		except:
			pass
		
		try:
			self._handle_out('privmsg', server, target, [message])
			self._servers[server].privmsg(target, message)
		except:
			print("gbot.irc privmsg fail:")
			print((' '*self.bot.indent) + 'server:', server)
			print((' '*self.bot.indent) + 'target:', target)
			print((' '*self.bot.indent) + 'message:', message)
			
	def action(self, server, target, action):
		""" Send a /me to the target."""
		try: #overload target, so user can use event.source() directly
			target = target.split('!')[0]
		except:
			pass
		
		try:
			self._handle_out('action', server, target, [action])
			self._servers[server].action(target, action)
		except:
			print("gbot.irc action fail:")
			print((' '*self.bot.indent) + 'server:', server)
			print((' '*self.bot.indent) + 'target:', target)
			print((' '*self.bot.indent) + 'message:', message)
	
	def join(self, server, channel, password=None):
		""" Join the given channel, on given server."""
		try:
			#self._handle_out('join', server, channel)
			self._servers[server].join(channel)
		except:
			print("gbot.irc join fail:")
			print((' '*self.bot.indent) + 'server:', server)
			print((' '*self.bot.indent) + 'channel:', channel)
	
	def quit(self, server, message):
		""" Quit from the given server using the message provided."""
		try:
			self._handle_out('quit', server, None, [message])
			self._servers[server].quit(message)
			del self._servers[server]
		except:
			print("gbot.irc quit fail:")
			print((' '*self.bot.indent) + 'server:', server)
			print((' '*self.bot.indent) + 'message:', message)
		
		if len(self._servers) < 1:
			print('goodbye')
			sys.exit()
	
	def ctcp_reply(self, server, ip, string):
		""" Send a CTCP Reply."""
		try:
			self._handle_out('ctcp', server, ip, [string])
			self._servers[server].ctcp_reply(ip, string)
		except:
			print("gbot.irc ctcp_reply fail:")
			print((' '*self.bot.indent) + 'server:', server)
			print((' '*self.bot.indent) + 'ip:', ip)
			print((' '*self.bot.indent) + 'string:', string)
	
	
	def process_forever(self):
		""" All's configured, pass control over to irclib."""
		self._irc.process_forever()
