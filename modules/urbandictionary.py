#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
import urllib.request, urllib.parse, urllib.error
import json


class urbandictionary(Module):
    """Allows access to UrbanDictionary."""

    def cmd_ud(self, event, command, usercommand):
        """See UrbanDictionary definition

        @usage <query>
        """
        encoded_query = urllib.parse.urlencode({b'term': unescape(usercommand.arguments)})
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
