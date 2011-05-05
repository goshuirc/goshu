#!/usr/bin/env python
"""
google.py - Goshubot google Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module
from gbot.helper import splitnum
import urllib.request, urllib.parse, urllib.error
import json

class Google(Module):
	
	name = "Google"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'google' : [self.google, 'google something, get results', 0],
			},
		}
	
	def google(self, query, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		if channel == self.bot.nick:
			channel = nick
		
		encoded_query = urllib.parse.urlencode({b'q' : query})
		url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (encoded_query)
		
		search_results = urllib.request.urlopen(url)
		json_result = json.loads(search_results.read().decode('utf-8'))
		try:
			url_result = json_result['responseData']['results'][0]['unescapedUrl']
		except:
			url_result = 'No Results'
		
		output = '*** Google: '+url_result
		
		self.bot.irc.privmsg(server, channel, output)
