#!/usr/bin/env python
"""
irc.py - Goshubot irclib Wrapper
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

import libs.irclib
libs.irclib.DEBUG = True

class IRC(object):
	""" Acts as a wrapper for irclib."""
	
	def __init__(self):
		self._events = {
			'in' : {
				#'motd' : [modules.log, etc],
			},
			'out' : {
				#'msg' : [modules.log, etc],
			},
			'commands' : {
				#'8ball' : [modules.ball, etc],
			},
		}
		""" Events affect all servers."""
		self._irc = libs.irclib.IRC()
		self._servers = {
			#'example' : irclib_ServerConnection,
		}
		""" List of servers we are currently connected to."""
		self._irc.add_global_handler('all_events', self._handle_irclib)
	
	def connect(self, server_nickname, server, port, nickname, password=None,
				username=None, ircname=None, localaddress="", localport=0):
		""" Connects to the given server."""
		current_server = self._irc.server()
		current_server.connect(server, port, nickname, password, username,
							 ircname, localaddress, localport)
		self._servers[server_nickname] = current_server
		return current_server
	
	def connect_dict(self, dictionary):
		for server in dictionary:
			server_nickname = server
			server_address = dictionary[server]['address']
			server_ssl = dictionary[server]['ssl']
			server_port = dictionary[server]['port']
			bot_nick = dictionary[server]['bot_nick']
			self.connect(server_nickname, server_address, server_port, bot_nick)
	
	def connection_prompt(self, dictionary=None):
		""" Prompt for server/channel connection details."""
		dictionary_out = {}
		more_servers = True
		while more_servers:
			server_nickname = raw_input('Server Nickname: ')
			dictionary_out[server_nickname] = {}
			dictionary_out[server_nickname]['address'] = raw_input('Server Address (irc.example.com): ')
			
			if False: #ssl not handled within irclib yet
				ssl = ''
				while ssl != 'y' and ssl != 'n':
					ssl = raw_input('SSL? (y/n)')
			
				if ssl == 'y':
					dictionary_out[server_nickname]['ssl'] = True
					assumed_port = 6697
				else:
					dictionary_out[server_nickname]['ssl'] = False
					assumed_port = 6667
			dictionary_out[server_nickname]['ssl'] = False
			assumed_port = 6667
			
			port = 'portnumberhere'
			while port.isdigit() == False and port != '':
				port = raw_input('Port ['+str(assumed_port)+']:')
			
			if port == '':
				dictionary_out[server_nickname]['port'] = assumed_port
			else:
				dictionary_out[server_nickname]['port'] = int(port)
			
			bot_nick = raw_input('Bot Nick: ')
			dictionary_out[server_nickname]['bot_nick'] = bot_nick
			
			print server_nickname, 'configured'
			
			more = ''
			while more != 'y' and more != 'n':
				more = raw_input('Would you like to configure more connections? ')
			
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
	
	def add_handler(self, direction, command, handler):
		""" Add a function that handles an internal event."""
		try:
			self._events[direction][command].append(handler)
		except KeyError:
			self._events[direction][command] = []
			self._events[direction][command].append(handler)
		except:
			print "gbot.irc add_handler fail:"
			print self.indent + 'direction:', direction
			print self.indent + 'command:', command
			print self.indent + 'handler:', handler
	
	def add_command(self, command, description, handler, access_level=0):
		""" Add a function that responds to a said command."""
		pass
	
	def _handle_irclib(self, connection, event):
		"""[Internal]"""
		pass
	
	
	def privmsg(self, server, target, message):
		""" Send a private message to target, on given server."""
		# call internal event
		try:
			self._servers[server].privmsg(target, message)
		except:
			print "gbot.irc privmsg fail:"
			print self.indent + 'server:', server
			print self.indent + 'target:', target
			print self.indent + 'message:', message
	
	
	def process_forever(self):
		""" All's configured, pass control over to irclib."""
		self._irc.process_forever()
