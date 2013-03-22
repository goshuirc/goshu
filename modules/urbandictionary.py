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


class urbandictionary(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands' : {
                'ud' : [self.ud_search, '<query> --- see UrbanDictionary definition'],
            },
        }

    def ud_search(self, event, command, usercommand):
        encoded_query = urllib.parse.urlencode({b'term' : unescape(usercommand.arguments)})
        url = 'http://www.urbandictionary.com/iphone/search/define?%s' % (encoded_query)
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = escape(str(json_result['list'][0]['word'])).replace('\r', '').replace('\n', ' ').strip()
                url_result += ' --- '
                url_result += escape(str(json_result['list'][0]['definition'])).replace('\r', '').replace('\n', ' ').strip()
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'

        response = '*** UrbanDictionary: ' + url_result

        self.bot.irc.msg(event, response)
