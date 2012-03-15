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
import urllib.request, urllib.parse, urllib.error

class google(Module):
    name = 'google'

    def __init__(self):
        self.events = {
            'commands' : {
                '*' : [self.dynamic_search, '--- dynamic searches', 0],
                'google' : [self.google_search, '<query> --- google something, get results', 0],
            },
        }
        self.dynamic_path = 'modules'+os.sep+'google'

    def commands(self):
        output = Module.commands(self)
        for (dirpath, dirs, files) in os.walk(self.dynamic_path):
            for file in files:
                try:
                    (name, ext) = os.path.splitext(file)
                    if ext == os.extsep + 'json':
                        info = json.loads(open(dirpath+os.sep+file).read())
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

                output[name] = [self.dynamic_search, command_description, command_permission]
        return output


    def dynamic_search(self, event, command):
        module_path = None
        for (dirpath, dirs, files) in os.walk(self.dynamic_path):
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
            responses = json.loads(open(module_path+os.sep+filename_escape(command.command)+os.extsep+'json').read())
        except ValueError:
            return

        query = ''
        if 'url' in responses:
            query += 'site:' + responses['url'] + ' '
        query += command.arguments

        if 'name' in responses:
            name = responses['name']
        else:
            name = 'Search'
        response = '*** ' + name + ': '
        response += self.google_result_search(query)

        self.bot.irc.servers[event.server].privmsg(event.from_to, response)

    def google_search(self, event, command):
        response = '*** /c12G/c4o/c8o/c12g/c3l/c4e/c: '

        calc_result = self.google_calc_search(command.arguments)
        if calc_result:
            response += calc_result
        else:
            response += self.google_result_search(command.arguments)

        self.bot.irc.servers[event.server].privmsg(event.from_to, response)


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
        return url_result

    def google_calc_search(self, query):
        url = 'https://www.google.com/ig/calculator?'
        url += urllib.parse.urlencode({b'q' : unescape(query)})

        try:
            calc_result = urllib.request.urlopen(url)
            calc_read = calc_result.read().decode('utf-8')
            calc_split = calc_read.split('"')

            #q_from = json_result['lhs']
            #q_to = json_result['rhs']
            q_from = calc_split[1]
            q_to = calc_split[3]
            if q_from == '' or q_to == '':
                return False
            final_result = '/i' + escape(q_from) + '/i is /i' + escape(q_to) + '/i'
        except:
            final_result = False

        return final_result
