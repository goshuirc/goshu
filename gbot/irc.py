#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a soda in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot	-	http://danneh.net/goshu

from .libs import girclib

class IRC(girclib.IRC):
	"""Manages goshubot's IRC communications."""
	
	def __init__(self, bot):
		girclib.IRC.__init__(self)
		self.bot = bot
	
	def connect_info(self, info, settings):
		for name in info._store:
			try:
				srv_nick = info._store[name]['connection']['nick']
			except KeyError:
				srv_nick = settings._store['nick']
			
			srv_address = info._store[name]['connection']['address']
			srv_port = info._store[name]['connection']['port']
			
			try:
				srv_password = info._store[name]['connection']['password']
			except KeyError:
				srv_password = None
			
			try:
				srv_username = info._store[name]['connection']['username']
			except:
				srv_username = None
			
			try:
				srv_ircname = info._store[name]['connection']['ircname']
			except:
				srv_ircname = None
			
			try:
				srv_localaddress = info._store[name]['connection']['localaddress']
				srv_localport = info._store[name]['connection']['localport']
			except:
				srv_localaddress = ""
				srv_localport = 0
			
			try:
				srv_ssl = info._store[name]['connection']['ssl']
			except:
				srv_ssl = False
			
			try:
				srv_ipv6 = info._store[name]['connection']['ipv6']
			except:
				srv_ipv6 = False
			
			s = self.server(name)
			s.connect(srv_address, srv_port, srv_nick, srv_password, srv_username, srv_ircname, srv_localaddress, srv_localport, srv_ssl, srv_ipv6)
			
			if 'nickserv_password' in info._store[name]['connection']:
				s.privmsg('nickserv', 'identify '+info._store[name]['connection']['nickserv_password'])
			
			if 'autojoin_channels' in info._store[name]['connection']:
				for channel in info._store[name]['connection']['autojoin_channels']:
					s.join(channel)