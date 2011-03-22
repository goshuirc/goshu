#!/usr/bin/env python
"""
irc.py - Goshubot irclib Wrapper
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from helper import splitnum
import libs.irclib
libs.irclib.DEBUG = True

class IRC(object):
	""" Acts as a wrapper for irclib. Highly convoluded wrapper, perhaps, but it
		is required so we can trap outgoing events."""
	
	def __init__(self, bot):
		self.bot = bot
		
		""" Events affect all servers."""
		self._irc = libs.irclib.IRC()
		self._servers = {
			#'example' : irclib.ServerConnection,
		}
		""" List of servers we are currently connected to."""
		self._irc.add_global_handler('all_events', self._handle_irclib)
		self._irc.add_global_handler('privmsg', self._handle_command)
		self._irc.add_global_handler('pubmsg', self._handle_command)
	
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
		if dictionary != None:
			dictionary_out.update(dictionary)
			for server in dictionary:
				print server+':'
				print ' '+dictionary[server]['address']+':'+str(dictionary[server]['port'])
				if dictionary[server]['ssl']:
					ssl = 'Enabled'
				else:
					ssl = 'Disabled'
				#print ' SSL', ssl #save for when ssl actually works
				print ''
			
			more = ''
			while more != 'y' and more != 'n':
				more = raw_input('Would you like to configure more connections? ')
			
			if more == 'y':
				more_servers = True
			else:
				more_servers = False
		
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
	
	
	def _handle_irclib(self, connection, event):
		"""[Internal]"""
		handler_functions = self.modules.handlers('in', event.eventtype())
		for handler in handler_functions:
			handler(connection, event)
	
	def _handle_command(self, connection, event):
		"""[Internal]"""
		(command, args) = (None, None)
		if event.arguments()[0].split(self.bot.prefix)[0] == '': #command for us
			command = event.arguments()[0].split(self.bot.prefix)[1]
			(command, args) = splitnum(command, 1)
			
		handler_functions = self.modules.handlers('commands', command)
		for handler in handler_functions:
			handler[0](args, connection, event)
	
	def _event(self, event):
		pass
	
	
	def privmsg(self, server, target, message):
		""" Send a private message to target, on given server."""
		# call internal event
		try:
			target = target.split('!')[0]
		except:
			pass
		
		try:
			self._servers[server].privmsg(target, message)
		except:
			print "gbot.irc privmsg fail:"
			print self.indent + 'server:', server
			print self.indent + 'target:', target
			print self.indent + 'message:', message
	
	def join(self, server, channel, password=None):
		""" Join the given channel, on given server."""
		self._servers[server].join(channel)
	
	
	def process_forever(self):
		""" All's configured, pass control over to irclib."""
		self._irc.process_forever()
