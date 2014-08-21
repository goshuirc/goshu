#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
from gbot.libs.helper import html_unescape
import json
import urllib.request, urllib.parse, urllib.error
import socket


class google(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                ('google', 'g'): [self.google_search, '<query> --- google something, get results'],
            },
        }

    def google_search(self, event, command, usercommand):
        response = '*** @c12G@c4o@c8o@c12g@c3l@c4e@c: {}'.format(self.google_result_search(usercommand.arguments))

        self.bot.irc.msg(event, response, 'public')

    def google_result_search(self, query):
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
        url += urllib.parse.urlencode({b'q': unescape(query)})

        try:
            search_results = urllib.request.urlopen(url)
            try:
                json_result = json.loads(search_results.read().decode('utf-8'))
                url_result = escape(html_unescape(json_result['responseData']['results'][0]['titleNoFormatting']))
                url_result += ' -- '
                url_result += escape(json_result['responseData']['results'][0]['unescapedUrl'])
            except:
                url_result = 'No Results'

        except urllib.error.URLError:
            url_result = 'Connection Error'

        except socket.timeout:
            url_result = 'Connection timed out'

        return url_result
