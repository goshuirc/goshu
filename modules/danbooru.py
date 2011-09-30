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
import sys
import os

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
        except ValueError:
            return
        
        if 'display_name' in booru:
            response = booru['display_name']
        else:
            response = '*** BooruNameHere: '
        
        if 'url' not in booru:
            return
        response += self.retrieve_url(booru['url'], command.arguments)
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)
    
    
    def retrieve_url(self, url, tags):
        encoded_tags = urllib.parse.urlencode({
            b'limit' : 1,
            b'tags' : unescape(tags),
        })
        api_url = url + '/post/index.json?' + encoded_tags
        
        try:
            search_results = urllib.request.urlopen(api_url)
        except:
            return 'Connection Error'
        
        results_http = search_results.read().decode('utf-8')
        
        results_json = json.loads(results_http)
        
        try:
            return escape(url + '/post/show/' + str(results_json[0]['id']))
        except:
            return 'No Results'