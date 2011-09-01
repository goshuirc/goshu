#!/usr/bin/env python
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
import json

class list(Module):
    name = "list"
    
    def __init__(self):
        self.events = {
            'commands' : {
                'list' : [self.list, "[command] --- list all commands; if command is present, display info on that command instead~", 0],
            },
        }
    
    def list(self, event, command):
        bot_commands = []
        
        for module in self.bot.modules.modules:
            module_commands = self.bot.modules.modules[module].commands()
            for command_name in module_commands:
                command_description = module_commands[command_name][1]
                command_permission = module_commands[command_name][2]
                if command_permission <= 0:
                    bot_commands.append([command_name, command_description, command_permission])
        bot_commands = sorted(bot_commands)
        
        if command.arguments:
            # single command info
            for bot_command in bot_commands:
                if bot_command[0] == command.arguments.split()[0]:
                    output = '*** Command:  '
                    output += bot_command[0] + ' '
                    output += bot_command[1]
                    
                    self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], output)
        
        else:
            # list commands
            output = '*** Commands: '
            for bot_command in bot_commands:
                output += bot_command[0] + ', '
            output = output[:-2] # remove last ', '
            
            self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], output)