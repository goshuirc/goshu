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
from gbot.libs.helper import filename_escape
import urllib.request, urllib.parse, urllib.error
import json
import os
from pprint import pprint

class dictionary(Module):
    name = 'dictionary'

    def __init__(self):
        self.events = {
            'commands' : {
                'def' : [self.dictionary_definition, '<word> --- returns word definition', 0],
            },
        }

    def dictionary_definition(self, event, command):
        if command.arguments.strip() == '':
            return

        try:
            dictionary_info = json.loads(open('config'+os.sep+'modules'+os.sep+filename_escape(self.name)+os.extsep+'json').read())
        except:
            print('no api key file')
            return

        url = 'http://api.wordnik.com/v4/word.json/'
        url += urllib.parse.urlencode({b'' : unescape(command.arguments.strip())})[1:]
        url += '/definitions?'
        url += urllib.parse.urlencode({
            b'limit' : b'1',
            b'useCanonical' : b'true',
            b'api_key' : dictionary_info['api_key'],
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

        except urllib.error.HTTPError as error_code:
            if '404' in error_code:
                response += 'No Search Terms'

            elif '401' in error_code:
                response += 'API Key Auth Fail'

            else:
                response += str(error_code)

        except IndexError:
            response += 'Definition Not Found'

        self.bot.irc.servers[event.server].privmsg(event.from_to, response)
