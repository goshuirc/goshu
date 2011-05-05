#!/usr/bin/env python
"""
gelbooru.py - Goshubot gelbooru Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module
from gbot.helper import splitnum
import urllib.request, urllib.parse, urllib.error
import re

class Gelbooru(Module):
	
	name = "Gelbooru"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'gelbooru' : [self.gelbooru, 'return gelbooru result for given tags', 0],
			},
		}
	
	def gelbooru(self, tags, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		if channel == self.bot.nick:
			channel = nick
		
		encoded_tags = urllib.parse.urlencode({
			b'limit' : 1,
			b'tags' : tags,
		})
		url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&%s' % (encoded_tags)
		
		try:
			search_results = urllib.request.urlopen(url)
		except:
			output = '*** Gelbooru: Offline'
			self.bot.irc.privmsg(server, channel, output)
			return
		
		results_http = search_results.read().decode('utf-8')
		
		regex = re.compile('id="(\d+)"')
		results_regex = regex.findall(results_http)
		
		try:
			result = results_regex[0]
			output = '*** Gelbooru: http://www.gelbooru.com/index.php?page=post&s=view&id='+result
		except:
			output = '*** Gelbooru: No Results'
		
		self.bot.irc.privmsg(server, channel, output)
