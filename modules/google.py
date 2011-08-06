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

class google(Module):
    name = 'google'
    
    def __init__(self):
        self.events = {
            'commands' : {
                'google' : [self.google_search, '<query> --- google something, get results', 0],
                'youtube' : [self.youtube_search, '<query> --- searches, then returns youtube video', 0],
            },
        }
    
    def google_search(self, event, command):
        encoded_query = urllib.parse.urlencode({b'q' : unescape(command.arguments)})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (encoded_query)
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = escape(json_result['responseData']['results'][0]['unescapedUrl'])
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'
        
        response = '*** /c12G/c4o/c8o/c12g/c3l/c4e/c: ' + url_result
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)
    
    def youtube_search(self, event, command):
        encoded_query = urllib.parse.urlencode({b'q' : unescape(command.arguments)})
        url = 'http://gdata.youtube.com/feeds/api/videos?alt=jsonc&v=2&max-results=1&%s' % (encoded_query)
        
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = json_result['data']['items'][0]['title']
                url_result += ' - http://www.youtube.com/watch?v='
                url_result += json_result['data']['items'][0]['id']
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'
        
        response = '*** You/c5Tube/c: '+url_result
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)