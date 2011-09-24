#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module, Command
from gbot.libs.girclib import escape, unescape
from gbot.libs.helper import filename_escape
import random
import os
import sys
import json

class responses(Module):
    name = 'responses'
    
    def __init__(self):
        self.events = {
            'in' : {
                'pubmsg' : [(0, self.combined_call)],
                'privmsg' : [(0, self.combined_call)],
            },
        }
        self.responses_path = 'modules'+os.sep+'responses'
        random.seed()
    
    
    def commands(self):
        output = Module.commands(self)
        for (dirpath, dirs, files) in os.walk(self.responses_path):
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

        # /s means source, the nick of whoever did the command
        # /t means target, either whoever they write afterwards, or the current self nick
        # note: /S and /T represent allcaps versions of /s and /t
        # /m at the start means: send this line as a /me rather than a /msg
    
    def combined_call(self, event):
        if event.arguments[0].split(self.bot.settings._store['prefix'])[0] == '':
            try:
                command_name = event.arguments[0][1:].split()[0].lower()
            except IndexError:
                return
            try:
                command_args = event.arguments[0][1:].split(' ', 1)[1]
            except IndexError:
                command_args = ''
            self.combined(event, Command(command_name, command_args))
    
    def combined(self, event, command):
        module_path = None
        for (dirpath, dirs, files) in os.walk(self.responses_path):
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
        
        source = event.source.split('!')[0]
        if command.arguments.strip() == '':
            target = self.bot.irc.servers[event.server].info['connection']['nick']
            num = '1'
        else:
            target = command.arguments.strip()
            if '2' in responses:
                num = '2'
            else:
                num = '1'
        
        if 'initial' in responses:
            output = [responses['initial']]
        else:
            output = []
        
        response_num = random.randint(1, len(responses[num])) - 1
        response = responses[num][response_num]
        if num + 'pre' in responses:
            response =  responses[num + 'pre'] + response
        if num + 'post' in responses:
            response += responses[num + 'post']
        output.append(response)
        
        for outline in output:
            outline = outline.replace('/S', source.upper()).replace('/T', target.upper())
            outline = outline.replace('/s', source).replace('/t', target)
            
            if outline[0:2] == '/m':
                self.bot.irc.servers[event.server].action(event.from_to, outline[2:].strip())
            else:
                self.bot.irc.servers[event.server].privmsg(event.from_to, outline)