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
import inspect
import imp
import importlib
import threading
import json


class Module:
    """Module to add commands/functionality to the bot."""

    def __init__(self):
        if not getattr(self, 'name', ''):
            self.name = self.__class__.__name__

        if not getattr(self, 'ext', ''):
            if len(self.name) >= 3:
                self.ext = self.name[:3]
            else:
                self.ext = self.name

        self.dynamic_path = 'modules'+os.sep+self.name

    def commands(self):
        # static commands
        commands = self.module_commands

        # dynamic commands
        for (dirpath, dirs, files) in os.walk(self.dynamic_path):
            for file in files:
                try:
                    (name, ext) = os.path.splitext(file)
                    if ext == os.extsep + 'json':
                        if os.path.splitext(name)[1] == os.extsep + self.ext:
                            info = json.loads(open(dirpath+os.sep+file).read())
                        else:
                            continue
                    else:
                        continue
                except ValueError:
                    continue

                if 'name' in info:
                    name = info['name']
                else:
                    name = os.path.splitext(os.path.splitext(file)[0])[0]

                if 'call' in info:
                    call = getattr(self, info['call'])
                else:
                    call = self.combined

                if 'desc' in info:
                    if isinstance(info['desc'], str):
                        desc = [info['desc']]
                    elif isinstance(info['desc'], list):
                        desc = info['desc']
                else:
                    desc = ''

                if 'call_level' in info:
                    call_level = info['call_level']
                else:
                    call_level = 0

                if 'view_level' in info:
                    view_level = info['view_level']
                else:
                    view_level = call_level

                if isinstance(name, list):  # aliases
                    commands[name[0]] = Command(call=call, desc=desc, call_level=call_level, view_level=view_level, json=info)

                    for command in name[1:]:
                        commands[command] = Command(call=call, desc=desc, call_level=call_level, view_level=view_level, json=info, alias=name[0])

                elif isinstance(name, str):
                    commands[name] = Command(call=call, desc=desc, call_level=call_level, view_level=view_level, json=info)

        return commands

    def combined(self, event, command, usercommand):
        ...

    def unload(self):
        ...


class Modules:
    """Manages goshubot's modules."""

    def __init__(self, bot):
        self.bot = bot
        self.whole_modules = {}
        self.modules = {}
        self.paths = []

    def add_path(self, path):
        if not path in sys.path:
            self.paths.append(path)
            sys.path.insert(0, path)

    def modules_from_path(self, path):
        modules = []
        for(dirpath, dirs, files) in os.walk(path):
            for file in files:
                (name, ext) = os.path.splitext(file)
                if ext == os.extsep + 'py':
                    modules.append(name)
        return modules

    def load_init(self, path):
        self.add_path(path)
        modules = self.modules_from_path(path)
        output = 'modules '
        for module in modules:
            loaded_module = self.load(module)
            if loaded_module is not None:
                output += ', '.join(self.whole_modules[module]) + ', '
            else:
                output += module + '[FAILED], '
        output = output[:-2]
        output += ' loaded'
        self.bot.curses.pad_addline(output)

    def load(self, name):
        whole_module = importlib.import_module(name)
        imp.reload(whole_module)  # so reloading works

        # find the actual goshu Module(s) we wanna load from the whole module
        modules = []
        for item in inspect.getmembers(whole_module):
            if item[1] in Module.__subclasses__():
                modules.append(item[1]())
                break
        if not modules:
            return False

        # if /any/ are dupes, exit
        for module in modules:
            if module.name in self.modules:
                return False

        self.whole_modules[name] = []

        for module in modules:
            self.whole_modules[name].append(module.name)
            self.modules[module.name] = module

            if not getattr(module, 'events', None):
                module.events = {}

            for direction in ['in', 'out', 'commands', '*']:
                if direction not in module.events:
                    module.events[direction] = {}

            module.module_commands = {}
            for command in module.events['commands']:
                self.add_command_info(module.name, command)
            module.folder_path = 'modules' + os.sep + name
            module.bot = self.bot

        return True

    def unload(self, name):
        if name not in self.whole_modules:
            self.bot.curses.pad_addline('module', name, 'not in', self.whole_modules)
            return False

        for modname in self.whole_modules[name]:
            self.modules[modname].unload()
            del self.modules[modname]

        del self.whole_modules[name]
        return True

    def handle(self, event):
        called = []
        for module in sorted(self.modules):
            for search_direction in ['*', event.direction]:
                for search_type in ['*', event.type]:
                    if search_type in self.modules[module].events[search_direction]:
                        for h in self.modules[module].events[search_direction][search_type]:
                            if h[1] not in called:
                                called.append(h[1])
                                if len(h) > 2 and h[2]:
                                    h[1](event)
                                else:
                                    threading.Thread(target=h[1], args=[event]).start()
        if event.type == 'privmsg' or event.type == 'pubmsg' and event.direction == 'in':
            self.handle_command(event)

    def handle_command(self, event):
        if event.arguments[0].startswith(self.bot.settings.store['prefix']):
            in_string = event.arguments[0][len(self.bot.settings.store['prefix']):].strip()
            if not in_string:
                return  # empty

            command_list = in_string.split(' ', 1)
            command_name = command_list[0].lower()

            if len(command_list) > 1:
                command_args = command_list[1]
            else:
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
                        module_commands = self.modules[module].commands()
                        if search_command in module_commands:
                            command_info = module_commands[search_command]

                            if userlevel >= command_info.call_level:
                                if command_info.call not in called:
                                    called.append(command_info.call)
                                    threading.Thread(target=command_info.call,
                                                     args=(event, command_info, UserCommand(command_name, command_args))).start()
                            else:
                                self.bot.curses.pad_addline('        No Privs')

    def add_command_info(self, module, name):
        info = self.modules[module].events['commands'][name]

        if isinstance(name, tuple):
            self.modules[module].module_commands[name[0]] = Command(info)

            for alias in name[1:]:
                self.modules[module].module_commands[alias] = Command(info, alias=name[0])

        elif isinstance(name, str):
            self.modules[module].module_commands[name] = Command(info)


class Command:
    """Goshubot command storage."""
    def __init__(self, base_info=None, **kwargs):
        if base_info:
            self.call = base_info[0]
            self.desc = base_info[1]
            self.call_level = base_info[2]

            if len(base_info) > 3:
                self.view_level = base_info[3]
            else:
                self.view_level = self.call_level

        if kwargs:
            for key in kwargs:
                setattr(self, key, kwargs[key])

        if not hasattr(self, 'alias'):
            self.alias = False

        if isinstance(self.desc, str):
            self.desc = [self.desc]


class UserCommand:
    """Command from a client."""

    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments
