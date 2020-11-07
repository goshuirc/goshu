#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import json
import os
import socket
import urllib.request, urllib.parse, urllib.error

from girc.formatting import escape, unescape
import hashlib

from gbot.libs.helper import filename_escape
from gbot.modules import Module


class danbooru(Module):

    def combined(self, event, command, usercommand):
        config_name = '{}.json'.format(filename_escape(self.name))
        boorufilename = os.sep.join(['config', 'modules', config_name])
        try:
            booruaccounts = json.loads(open(boorufilename, encoding='utf-8').read())
        except ValueError:
            self.bot.gui.put_line('danbooru: Danbooru Account info file error: {}'
                                  ''.format(boorufilename))
            return
        except IOError:
            self.bot.gui.put_line('danbooru: Danbooru Account info file not found, ignoring: {}'
                                  ''.format(boorufilename))
            booruaccounts = {}

        if 'display_name' in command.json:
            display_name = command.json['display_name']
        else:
            display_name = usercommand.command

        response = '*** {name}: '.format(name=display_name)

        if 'url' not in command.json:
            return

        if 'version' not in command.json:
            command.json['version'] = 1

        if usercommand.command in booruaccounts:
            username = booruaccounts[usercommand.command]['username']
            password = booruaccounts[usercommand.command]['password']
        else:
            username = None
            password = None

        response += self.retrieve_url(command.json['url'],
                                      usercommand.arguments,
                                      command.json['version'],
                                      username, password)

        event['from_to'].msg(response)

    def retrieve_url(self, url, tags, version, username=None, password=None):
        post = {
            b'limit': 1,
            b'tags': unescape(tags),
        }

        if username:
            post['login'] = username

        if password:
            # choujin-steiner junk is because that's how danbooru hashes their passwords
            post['password_hash'] = str(hashlib.sha1(b'choujin-steiner--' + password.encode('utf-8') + b'--').hexdigest())

        encoded_tags = urllib.parse.urlencode(post)

        # version
        if version == 1:
            api_position = '/post/index.json?'
        elif version == 2:
            api_position = '/posts.json?'
        api_url = url + api_position + encoded_tags

        try:
            search_results = urllib.request.urlopen(api_url)

        except socket.timeout:
            return 'Connection timed out'

        except urllib.error.URLError:
            return 'Connection Error'

        results_http = search_results.read().decode('utf-8')

        try:
            results_json = json.loads(results_http)

        except ValueError:
            return "Not a JSON response"

        try:
            return_str = escape(url + '/post/show/' + str(results_json[0]['id']))
            return_str += '  rating:$b' + results_json[0]['rating'] + '$b'
            # if version == 1:
            #     return_str += '  $c14' + results_json[0]['tags']
            # elif version == 2:
            #     return_str += '  $c14' + results_json[0]['tag_string']
            return return_str
        except:
            return 'No Results'
