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
import urllib.request, urllib.parse, urllib.error
import socket  # for timeout
from pyquery import PyQuery as pq
import json
import sys
import os


class apiquery(Module):

    def combined(self, event, command, usercommand):
        url = command.json['url']
        if usercommand.arguments == '':
            usercommand.arguments = ' '

        url = url.replace('@{escaped_query}', urllib.parse.urlencode({b'q' : unescape(usercommand.arguments)})[2:])

        if 'urlpost' in command.json:
            url += command.json['urlpost']

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Goshubot IRC bot'})
            query_results = urllib.request.urlopen(req, timeout=5)  # seconds
            query_read = query_results.read().decode('utf-8')

            try:
                if command.json['format'] == 'json':
                    json_results = json.loads(query_read)

                    if 'html_unescape' in command.json:
                        do_unescape = command.json['html_unescape']
                    else:
                        do_unescape = False

                    result = self.json_data_exctact(json_results, command.json['response'], do_unescape)

                elif command.json['format'] == 'xml':
                    # xmlns replace is a fix for lxml, here: https://bitbucket.org/olauzanne/pyquery/issue/17
                    query_xmlsafe = query_read.replace(' xmlns:', ' xmlnamespace:').replace(' xmlns=', ' xmlnamespace=')
                    result = self.xml_data_extract(query_xmlsafe, command.json['response'])

                else:
                    raise ApiQueryError

            except ApiQueryError:
                result = 'No Results'
        except urllib.error.URLError:
            result = 'Connection Error'
        except ValueError:
            result = 'No Results'
        except socket.timeout:
            result = 'Connection timed out'

        if 'display_name' in command.json:
            name = command.json['display_name']
        else:
            name = command.command

        response = '*** {name}: {result}'.format(name=name, result=result)
        self.bot.irc.msg(event, response, 'public')

    def json_data_exctact(self, results, response_format, do_unescape=False):
        response = ''

        for term in response_format:
            if term[0] == 'text':
                response += term[1]
            elif term[0] == 'escaped_text':
                response += escape(term[1])
            else:
                try:
                    # todo: Really, no better way than to eval?
                    if do_unescape:
                        response += escape(html_unescape(str(eval('results' + term[1]))))
                    else:
                        response += escape(str(eval('results' + term[1])))
                except IndexError:
                    raise ApiQueryError
                except KeyError:
                    raise ApiQueryError

        return response.replace('\n', ' ')

    def xml_data_extract(self, results, response_format):
        pq_results = pq(results)
        response = ''

        try:
            for term in response_format:
                if term[0] == 'text':
                    response += term[1]
                elif term[0] == 'escaped_text':
                    response += escape(term[1])
                elif term[0] == 'jquery':
                    response += pq_results(term[1]).text()
                elif term[0] == 'jquery_attr':
                    response += pq_results(term[1]).attr(term[2])
        except TypeError:
            raise ApiQueryError

        return response


class ApiQueryError(Exception):
    ...
