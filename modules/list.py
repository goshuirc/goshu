#!/usr/bin/env python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module

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
                if command_name == '*':
                    continue
                command_description = module_commands[command_name][1]
                command_permission = module_commands[command_name][2]
                if len(module_commands[command_name]) >= 4:
                    command_view_permission = module_commands[command_name][3]
                else:
                    command_view_permission = command_permission
                if self.bot.accounts.access_level(self.bot.accounts.account(event.source, event.server)) >= command_view_permission:
                    bot_commands.append([command_name, command_description, command_permission])
        bot_commands = sorted(bot_commands)

        if command.arguments:
            # single command info
            for bot_command in bot_commands:
                if bot_command[0] == command.arguments.split()[0]:
                    
                    # fix help display for single help strings
                    if isinstance(bot_command[1], str):
                        bot_command[1] = [bot_command[1]]

                    for help_string in bot_command[1]:
                        output = '*** Command:  ' + self.bot.settings.store['prefix']
                        output += bot_command[0] + ' '
                        output += help_string

                        self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], output)

        else:
            # list commands
            output = ['*** Commands: ']
            i = 0
            limit = 350
            for bot_command in bot_commands:
                if (len(output[i]) + len(bot_command[0])) > limit:
                    output.append('    ')
                    i += 1
                output[i] += bot_command[0] + ', '
            output[i] = output[i][:-2] # remove last ', '

            output.append('Note: to display information on a specific command, use /i'+self.bot.settings.store['prefix']+'list <command>/i. eg: /i'+self.bot.settings.store['prefix']+'list 8ball');

            for line in output:
                self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], line)
