#!/usr/bin/env python
"""
urbandictionary.py - Goshubot urbandictionary Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
from gbot.helper import splitnum
import urllib.request, urllib.parse, urllib.error
import re

class UrbanDictionary(Module):
	
	name = "UrbanDictionary"
	
	def __init__(self):
		self.events = {
			#'in' : {},
			#'out' : {},
			'commands' : {
				'ud' : [self.ud, 'return urban dictionary result for given query', 0],
			},
		}
	
	def ud(self, query, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		if channel == self.bot.nick:
			channel = nick
		
		encoded_query = urllib.parse.urlencode({
			b'term' : query,
		})
		url = 'http://www.urbandictionary.com/define.php?%s' % (encoded_query)
		
		try:
			search_results = urllib.request.urlopen(url)
		except:
			output = '*** UrbanDictionary: Error'
			self.bot.irc.privmsg(server, channel, output)
			return
			
		results_http = search_results.read().decode('utf-8')
		
		# regex taken from https://github.com/raqqa/Supybot-Plugins
		# we thank him for his unwitting involvment in this incidious plot
		regex = re.compile('.*class="definition"\>(.*)\<\/div\>\<di')
		results_regex = regex.findall(results_http)
		
		try:
			results_regex[0] = results_regex[0].strip()
			
			results_definition = ''
			still_parsing = True
			if results_regex[0][1] == '.':
				if results_regex[0][0].isalpha():
					results_definition = results_regex[0][0:2]
					results_regex[0] = results_regex[0][2:]
				else:
					results_regex[0] = results_regex[0][2:]
				results_regex[0] = results_regex[0].strip()
		
			while still_parsing:
				char = results_regex[0][0]
		
				if char == '<':
					tag = ''
					while char != '>':
						results_regex[0] = results_regex[0][1:] #strip first char
						char = results_regex[0][0]
						tag += char
					results_regex[0] = results_regex[0][1:] #strip first char
					char = results_regex[0][0]
					tag = tag[:-1]
				
					if tag == 'br':
						still_parsing = False
			
				if char == '.':
					try:
						if results_regex[0][1] == '.':
							results_definition += '...'
							still_parsing = False
				
						else:
							still_parsing = False
					except:
						still_parsing = False
			
				else:
					results_definition += char
					results_regex[0] = results_regex[0][1:]
		
				if len(results_regex[0]) < 1:
					still_parsing = False
	
			if results_definition[-1] == '.' and results_definition[-2] != '.':
				results_definition = results_definition[:-1]
		
			output = '*** UrbanDictionary: %s - %s' % (query, results_definition)
		
		except:
			output = '*** UrbanDictionary: No Results'
		
		self.bot.irc.privmsg(server, channel, output)
