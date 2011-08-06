#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a soda in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
import urllib.request, urllib.parse, urllib.error
import json

class danbooru(Module):
    name = 'danbooru'
    
    def __init__(self):
        self.events = {
            'commands' : {
                'danbooru' : [self.booru, '<tags> --- search danbooru result for given tags', 0],
                'oreno' : [self.booru, '<tags> --- search oreimo result for given tags', 0],
            },
        }
    
    def booru(self, event, command):
        if command.command == 'danbooru':
            url = 'http://danbooru.donmai.us'
            response = '*** Danbooru: '
        elif command.command == 'oreno':
            url = 'http://oreno.imouto.org'
            response = '*** OreNo: '
        response += self.retrieve_url(url, command.arguments)
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)
    
    def retrieve_url(self, url, tags):
        encoded_tags = urllib.parse.urlencode({
            b'limit' : 1,
            b'tags' : unescape(tags),
        })
        api_url = url + '/post/index.json?' + encoded_tags
        
        try:
            search_results = urllib.request.urlopen(api_url)
        except:
            return 'Connection Error'
        
        results_http = search_results.read().decode('utf-8')
        
        results_json = json.loads(results_http)
        
        try:
            return escape(url + '/post/show/' + str(results_json[0]['id']))
        except:
            return 'No Results'