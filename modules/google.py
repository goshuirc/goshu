#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from girc.formatting import escape, unescape

from gbot.modules import Module
from gbot.libs.helper import html_unescape
import json
import urllib.request, urllib.parse, urllib.error
import socket


class google(Module):
    """Lets users search using Google, provides a result."""

    def cmd_google(self, event, command, usercommand):
        """Google somethin, get results!

        @alias g
        @usage <query>
        """
        result = self.google_result_search(usercommand.arguments)
        response = '*** $c12G$c4o$c8o$c12g$c3l$c4e$c: {}'.format(result)

        event['from_to'].msg(response)

    def combined(self, event, command, usercommand):
        query = ''
        if 'url' in command.json:
            query += 'site:' + command.json['url'] + ' '
        query += usercommand.arguments

        if 'display_name' in command.json:
            name = command.json['display_name']
        else:
            name = usercommand.command
        response = '*** ' + name + ': '
        response += self.google_result_search(query)

        event['from_to'].msg(response)

    def google_result_search(self, query):
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
        url += urllib.parse.urlencode({b'q': unescape(query)})

        try:
            search_results = urllib.request.urlopen(url)
            try:
                json_result = json.loads(search_results.read().decode('utf-8'))
                html_result = json_result['responseData']['results'][0]['titleNoFormatting']
                url_result = escape(html_unescape(html_result))
                url_result += ' -- '
                url_result += escape(json_result['responseData']['results'][0]['unescapedUrl'])
            except:
                url_result = 'No Results'

        except urllib.error.URLError:
            url_result = 'Connection Error'

        except socket.timeout:
            url_result = 'Connection timed out'

        return url_result
