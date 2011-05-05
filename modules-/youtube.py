#!/usr/bin/env python
"""
youtube.py - Goshubot youtube Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module
from gbot.helper import splitnum
import urllib.request, urllib.parse, urllib.error
import json

class Youtube(Module):
	
	name = "Youtube"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'youtube' : [self.youtube, 'youtube something, get results', 0],
			},
		}
	
	def youtube(self, query, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		if channel == self.bot.nick:
			channel = nick
		
		encoded_query = urllib.parse.urlencode({b'q' : query})
		url = 'http://gdata.youtube.com/feeds/api/videos?alt=jsonc&v=2&max-results=1&%s' % (encoded_query)
		
		search_results = urllib.request.urlopen(url)
		json_result = json.loads(search_results.read().decode('utf-8'))
		try:
			url_result = json_result['data']['items'][0]['title']
			url_result += ' - http://www.youtube.com/watch?v='
			url_result += json_result['data']['items'][0]['id']
		except:
			url_result = 'No Results'
		
		output = '*** Youtube: '+url_result
		
		self.bot.irc.privmsg(server, channel, output)
