#!/usr/bin/env python
"""
irc.py - Goshubot irclib Wrapper
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

import libs.irclib
libs.irclib.DEBUG = True

class IRC:
	""" Acts as a wrapper for irclib."""
	
	def __init__(self):
		self._events = {
			'in' : {
				#'motd' : [modules.log, etc],
			},
			'out' : {},
			'commands' : {},
		}
		""" Events affect all servers."""
		self._irc = libs.irclib.IRC()
		self._servers = {
			#'example' : irclib_ServerConnection,
		}
		""" List of servers we are currently connected to."""
		self._irc.add_global_handler('all_events', self._handle_irclib)
	
	def connect(self, server_nickname, server, port, nickname, password=None, username=None,
				ircname=None, localaddress="", localport=0):
		""" Connects to the given server."""
		current_server = self._irc.server()
		current_server.connect(server, port, nickname, password, username,
							 ircname, localaddress, localport)
		self._servers[server_nickname] = current_server
		return current_server
	
	def process_forever(self):
		""" All's configured, pass control over to irclib."""
		self._irc.process_forever()
	
	
	def server_nick(self, server_connection):
		""" Returns the server nickname of the given connection."""
		for server in self._servers:
			if self._servers[server] == server_connection:
				return server
		return None
	
	def add_handler(self, direction, command, handler):
		try:
			self._events[direction][command].append(handler)
	
	def add_command(self, command, description, handler, access_level=0):
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
