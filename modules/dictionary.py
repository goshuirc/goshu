#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from girc.formatting import escape, unescape

from gbot.modules import Module
from gbot.libs.helper import filename_escape
import urllib.request, urllib.parse, urllib.error
import socket
import json
import os


class dictionary(Module):
    """Lets users ask for a word's definition."""

    def cmd_def(self, event, command, usercommand):
        """Returns word definition

        @usage <word>
        """
        if usercommand.arguments.strip() == '':
            return

        config_json = '{}.json'.format(filename_escape(self.name))
        dict_info_filename = os.sep.join(['config', 'modules', config_json])
        try:
            dictionary_info = json.loads(open(dict_info_filename).read())
        except:
            self.bot.gui.put_line('dictionary: No Wordnik API key file: {}'
                                  ''.format(dict_info_filename))
            return

        url = 'http://api.wordnik.com/v4/word.json/'
        url += urllib.parse.urlencode({b'': unescape(usercommand.arguments.strip())})[1:]
        url += '/definitions?'
        url += urllib.parse.urlencode({
            b'limit': b'1',
            b'useCanonical': b'true',
            b'api_key': dictionary_info['api_key'],
        })

        response = '*** Wordnik: '

        try:
            url_results = urllib.request.urlopen(url)
            json_result = json.loads(url_results.read().decode('utf-8'))
            response += escape(json_result[0]['word'])
            if 'partOfSpeech' in json_result[0]:
                response += ' ('
                response += escape(json_result[0]['partOfSpeech'])
                response += ')'
            response += ' --- '
            response += escape(json_result[0]['text'])

        except urllib.error.URLError:
            response += 'You broke it, nice job'

        except socket.timeout:
            response = 'Connection timed out'

        except urllib.error.HTTPError as error_code:
            if '404' in error_code:
                response += 'No Search Terms'

            elif '401' in error_code:
                response += 'API Key Auth Fail'

            else:
                response += str(error_code)

        except IndexError:
            response += 'Definition Not Found'

        event['from_to'].msg(response)
