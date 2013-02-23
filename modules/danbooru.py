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
import socket
import json
import os
import hashlib


class danbooru(Module):

    def combined(self, event, command, usercommand):
        try:
            booruaccounts = json.loads(open('config'+os.sep+'modules'+os.sep+filename_escape(self.name)+os.extsep+'json').read())
        except ValueError:
            return
        except IOError:
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

        response += self.retrieve_url(command.json['url'], usercommand.arguments, command.json['version'], username, password)

        self.bot.irc.msg(event, response, 'public')

    def retrieve_url(self, url, tags, version, username=None, password=None):
        post = {
            b'limit' : 1,
            b'tags' : unescape(tags),
        }

        if username:
            post['login'] = username

        if password:
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
            return_str += '  rating:@b' + results_json[0]['rating'] + '@b'
            #if version == 1:
            #    return_str += '  @c14' + results_json[0]['tags']
            #elif version == 2:
            #    return_str += '  @c14' + results_json[0]['tag_string']
            return return_str
        except:
            return 'No Results'
