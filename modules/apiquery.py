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
    name = 'apiquery'

    def __init__(self):
        self.events = {
            'commands' : {
                '*' : [self.combined, '<query> --- api query', 0],
            },
        }

    def commands(self):
        output = Module.commands(self)
        for (dirpath, dirs, files) in os.walk(self.folder_path):
            for file in files:
                try:
                    (name, ext) = os.path.splitext(file)
                    if ext == os.extsep + 'json':
                        info = json.loads(open(dirpath+os.sep+file).read())
                    else:
                        continue
                except ValueError:
                    continue

                if 'description' in info:
                    command_description = info['description']
                else:
                    command_description = ''
                if 'permission' in info:
                    command_permission = info['permission']
                else:
                    command_permission = 0

                output[name] = [self.combined, command_description, command_permission]
        return output

    def combined(self, event, command):
        module_path = None
        for (dirpath, dirs, files) in os.walk(self.folder_path):
            for file in files:
                if not dirpath in sys.path:
                    sys.path.insert(0, dirpath)
                (name, ext) = os.path.splitext(file)
                if ext == os.extsep + 'json':
                    if name == filename_escape(command.command):
                        module_path = dirpath
        if not module_path:
            return

        try:
            querydata = json.loads(open(module_path+os.sep+filename_escape(command.command)+os.extsep+'json').read())
        except ValueError:
            return

        url = querydata['url']
        if command.arguments == '':
            command.arguments = ' '

        url = url.replace('@{escaped_query}', urllib.parse.urlencode({b'q' : unescape(command.arguments)})[2:])

        if 'urlpost' in querydata:
            url += querydata['urlpost']

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Goshubot IRC bot'})
            query_results = urllib.request.urlopen(req, timeout=5)  # seconds
            query_read = query_results.read().decode('utf-8')

            try:
                if querydata['format'] == 'json':
                    json_results = json.loads(query_read)

                    if 'html_unescape' in querydata:
                        do_unescape = querydata['html_unescape']
                    else:
                        do_unescape = False

                    result = self.json_data_exctact(json_results, querydata['response'], do_unescape)

                elif querydata['format'] == 'xml':
                    # xmlns replace is a fix for lxml, here: https://bitbucket.org/olauzanne/pyquery/issue/17
                    query_xmlsafe = query_read.replace(' xmlns:', ' xmlnamespace:').replace(' xmlns=', ' xmlnamespace=')
                    result = self.xml_data_extract(query_xmlsafe, querydata['response'])

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

        response = '*** ' + querydata['name'] + ': ' + result
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
