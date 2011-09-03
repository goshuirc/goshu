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

class soundcloud(Module):
    name = 'soundcloud'
    
    def __init__(self):
        self.events = {
            'commands' : {
                'soundcloud' : [self.soundcloud_search, '<query> --- search soundcloud', 0],
            },
        }
    
    def soundcloud_search(self, event, command):
        encoded_query = urllib.parse.urlencode({b'q' : unescape(command.arguments)})
        url = 'http://api.soundcloud.com/tracks.json?client_id=e3dfa9998292005f9e73329b1dd9dfb7&%s' % (encoded_query)
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = escape(json_result[0]['title'])
                url_result += ' by '
                url_result += escape(json_result[0]['user']['username'])
                url_result += ' --- '
                url_result += escape(json_result[0]['permalink_url'])
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'
        
        response = '*** Soundcloud: ' + url_result
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)