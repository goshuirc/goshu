#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu
import os
import sys

class Module:
    """Module to add commands/functionality to the bot."""

    def commands(self):
        command_list = {}
        if 'commands' not in self.events:
            return command_list

        for command in self.events['commands']:
            command_list[command] = self.events['commands'][command]

        return command_list

class ModuleLoader:
    """Prepares a list of modules."""

    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for(dirpath, dirs, files) in os.walk(self.path):
            if not dirpath in sys.path:
                sys.path.insert(0, dirpath)
            for file in files:
                (name, ext) = os.path.splitext(file)
                if ext == os.extsep + 'py':
                    __import__(name, None, None, [''])

        for module in Module.__subclasses__():
            yield module()

class Modules:
    """Manages goshubot's modules."""

    def __init__(self, bot):
        self.bot = bot
        self.modules = {}

    def load(self, path):
        loader = ModuleLoader(path)
        output = 'modules '
        for module in loader:
            if self.append(module):
                output += module.name + ', '
        output = output[:-2]
        output += ' loaded'
        print(output)

    def append(self, module):
        if module not in self.modules:
            self.modules[module.name] = module
            for direction in ['in', 'out', 'commands', '*']:
                if direction not in module.events:
                    module.events[direction] = {}
            module.folder_path = 'modules' + os.sep + module.name
            module.bot = self.bot
            return True
        else:
            return False

    def handle(self, event):
        called = []
        for module in sorted(self.modules):
            for search_direction in ['*', event.direction]:
                for search_type in ['*', event.type]:
                    if search_type in self.modules[module].events[search_direction]:
                        for h in self.modules[module].events[search_direction][search_type]:
                            if h[1] not in called:
                                called.append(h[1])
                                h[1](event)
        if event.type == 'privmsg' or event.type == 'pubmsg' and event.direction == 'in':
            self.handle_command(event)

    def handle_command(self, event):
        if self.bot.settings.store['prefix'] in event.arguments[0] and event.arguments[0].split(self.bot.settings.store['prefix'])[0] == '':
            if len(event.arguments[0].split(self.bot.settings.store['prefix'])[1].strip()) < 1:
                return # empty
            elif len(event.arguments[0].split(self.bot.settings.store['prefix'])[1].split()[0]) < 1:
                return # no command
            command_name = event.arguments[0][1:].split()[0].lower()
            try:
                command_args = event.arguments[0][1:].split(' ', 1)[1]
            except IndexError:
                command_args = ''

            useraccount = self.bot.accounts.account(event.source, event.server)
            if useraccount:
                userlevel = self.bot.accounts.access_level(useraccount)
            else:
                userlevel = 0

            called = []
            for module in sorted(self.modules):
                if 'commands' in self.modules[module].events:
                    for search_command in ['*', command_name]:
                        if search_command in self.modules[module].events['commands']:
                            if userlevel >= self.modules[module].events['commands'][search_command][2]:
                                if self.modules[module].events['commands'][search_command][0] not in called:
                                    called.append(self.modules[module].events['commands'][search_command][0])
                                    self.modules[module].events['commands'][search_command][0](event, Command(command_name, command_args))
                            else:
                                print('no privs mang')

class Command:
    """Command from a client."""

    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments
