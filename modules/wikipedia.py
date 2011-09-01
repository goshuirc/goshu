#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
import urllib.request, urllib.parse, urllib.error
import json

class wikipedia(Module):
    name = 'wikipedia'
    
    def __init__(self):
        self.events = {
            'commands' : {
                'wiki' : [self.wikipedia_search, '<query> --- get Wikipedia article', 0],
            },
        }
    
    def wikipedia_search(self, event, command):
        if command.arguments == '':
            return
        
        query = {
            b'action' : 'query',
            b'list' : 'search',
            b'format' : 'json',
            b'srsearch' : unescape(command.arguments),
        }
        
        encoded_query = urllib.parse.urlencode(query)
        url = 'https://secure.wikimedia.org/wikipedia/en/w/api.php?%s' % (encoded_query)
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = escape('https://secure.wikimedia.org/wikipedia/en/wiki/') + escape(json_result['query']['search'][0]['title'])
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'
        
        response = '*** Wikipedia: ' + url_result
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)