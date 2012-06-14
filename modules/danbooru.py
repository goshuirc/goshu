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
import sys
import os
import hashlib

class danbooru(Module):
    name = 'danbooru'

    def __init__(self):
        self.events = {
            'commands' : {
                '*' : [self.combined, '--- handle danbooru', 0],
            },
        }
        self.booru_path = 'modules'+os.sep+'danbooru'


    def commands(self):
        output = Module.commands(self)
        for (dirpath, dirs, files) in os.walk(self.booru_path):
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
        for (dirpath, dirs, files) in os.walk(self.booru_path):
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
            booru = json.loads(open(module_path+os.sep+filename_escape(command.command)+os.extsep+'json').read())
            booruaccounts = json.loads(open('config'+os.sep+'modules'+os.sep+filename_escape(self.name)+os.extsep+'json').read())
        except ValueError:
            return
        except IOError:
            booruaccounts = {}

        if 'display_name' in booru:
            response = booru['display_name']
        else:
            response = '*** BooruNameHere: '

        if 'url' not in booru:
            return
        
        if 'version' not in booru:
            booru['version'] = 1
        
        if command.command in booruaccounts:
            booru['username'] = booruaccounts[command.command]['username']
            booru['password'] = booruaccounts[command.command]['password']
        else:
            booru['username'] = None
            booru['password'] = None
        
        response += self.retrieve_url(booru['url'], command.arguments, booru['version'],
                                      booru['username'], booru['password'])

        self.bot.irc.servers[event.server].privmsg(event.from_to, response)


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


        if version == 1:
            api_position = '/post/index.json?'
        elif version == 2:
            api_position = '/posts.json?'
        api_url = url + api_position + encoded_tags

        print(api_url)

        try:
            search_results = urllib.request.urlopen(api_url)
        except socket.timeout:
            result = 'Connection timed out'
        except:
            return 'Connection Error'

        results_http = search_results.read().decode('utf-8')

        try:
            results_json = json.loads(results_http)
        except ValueError:
            return "Not a JSON response"

        try:
            return_str = escape(url + '/post/show/' + str(results_json[0]['id']))
            return_str += '  rating:/b' + results_json[0]['rating'] + '/b'
            if version == 1:
                return_str += '  /c14' + results_json[0]['tags']
            elif version == 2:
                return_str += '  /c14' + results_json[0]['tag_string']
            return return_str
        except:
            return 'No Results'
