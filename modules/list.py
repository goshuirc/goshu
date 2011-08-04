#!/usr/bin/env python
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
import json

class list(Module):
    name = "list"
    
    def __init__(self):
        self.events = {
            'commands' : {
                'list' : [self.list, "['command] --- list commands/if 'command is present, display info on that command~", 0],
            },
        }
    
    def list(self, event, command):
        commands = []
        for module in self.bot.modules.handlers:
            for command_name in self.bot.modules.handlers[module]['commands']:
                command_description = self.bot.modules.handlers[module]['commands'][command_name][1]
                command_permission = self.bot.modules.handlers[module]['commands'][command_name][2]
                commands.append([command_name, command_description, command_permission])
        
        if command.arguments != '' and command.arguments[0] == self.bot.settings._store['prefix']:
            # info about specific command
            for command_list in commands:
                if command_list[0] == command.arguments[1:]:
                    output = '*** Command:  '
                    output += command_list[0]
                    output += ' '
                    output += command_list[1]
                    
                    self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], output)
        
        else:
            # command list
            output = '*** Commands: '
            for command_list in sorted(commands):
                if command_list[2] == 0:
                    output += command_list[0] + ', '
            output = output[:-2] # remove last ', '
            
            self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], output)