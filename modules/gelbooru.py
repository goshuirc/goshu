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

class gelbooru(Module):
    name = 'gelbooru'
    
    def __init__(self):
        self.events = {
            'commands' : {
                'gelbooru' : [self.booru, '<tags> --- search gelbooru result for given tags', 0],
            },
        }
    
    def booru(self, event, command):
        if command.command == 'gelbooru':
            url = 'http://gelbooru.com'
            response = '*** Gelbooru: '
        response += self.retrieve_url(url, command.arguments)
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)
    
    def retrieve_url(self, url, tags):
        encoded_tags = urllib.parse.urlencode({
            b'json' : 1,
            b'limit' : 1,
            b'tags' : unescape(tags),
        })
        api_url = url + '/index.php?page=dapi&s=post&q=index&' + encoded_tags
        
        try:
            search_results = urllib.request.urlopen(api_url)
        except:
            return 'Connection Error'
        
        results_http = search_results.read().decode('utf-8')
        
        results_json = json.loads(results_http)
        
        try:
            return escape(url + '/index.php?page=post&s=view&id=' + str(results_json[0]['id']))
        except:
            return 'No Results'