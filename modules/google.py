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
from gbot.libs.helper import filename_escape, html_unescape
import os
import sys
import json
import gbot.libs.demjson as demjson
import urllib.request, urllib.parse, urllib.error
import socket
import xml.sax.saxutils as saxutils


class google(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands' : {
                ('google', 'g'): [self.google_search, '<query> --- google something, get results'],
                ('calc', 'c'): [self.google_calc, '<expression> --- calculate something'],
            },
        }

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

        self.bot.irc.msg(event, response, 'public')

    def google_search(self, event, command, usercommand):
        response = '*** @c12G@c4o@c8o@c12g@c3l@c4e@c: {}'.format(self.google_result_search(usercommand.arguments))

        self.bot.irc.msg(event, response, 'public')

    def google_calc(self, event, command, usercommand):
        response = '*** @c12G@c4o@c8o@c12g@c3l@c4e@c: {}'.format(self.google_calc_search(usercommand.arguments))

        self.bot.irc.msg(event, response, 'public')

    def google_result_search(self, query):
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
        url += urllib.parse.urlencode({b'q' : unescape(query)})

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

    def google_calc_search(self, query):
        url = 'https://www.google.com/ig/calculator?'
        url += urllib.parse.urlencode({b'q' : unescape(query)})

        try:
            calc_result = urllib.request.urlopen(url)
            try:
                charset = calc_result.headers._headers[2][1].split('charset=')[1]
            except IndexError:
                charset = 'ISO-8859-1'
            calc_read = calc_result.read().decode(charset)

            json_result = demjson.decode(calc_read)
            q_from = json_result['lhs']
            q_to = saxutils.unescape(json_result['rhs'].replace('<sup>', '^').replace('</sup>', '').replace('&#215;', '×'))

            if q_from == '' or q_to == '':
                return 'Invalid expression'
            final_result = '@i' + escape(q_from) + '@i is @i' + escape(q_to) + '@i'
        except:
            final_result = 'Invalid expression'

        return final_result
