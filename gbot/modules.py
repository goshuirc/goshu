#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import os
import sys
import imp
import inspect
import importlib
import threading
from .libs.helper import JsonHandler


class Module:
    """Module to add commands/functionality to the bot."""

    def __init__(self, bot):
        self.bot = bot

        if not getattr(self, 'name', None):
            self.name = self.__class__.__name__

        if not getattr(self, 'ext', None):
            if len(self.name) >= 3:
                self.ext = self.name[:3]
            else:
                self.ext = self.name

        self.dynamic_path = '.' + os.sep + 'modules' + os.sep + self.name

        self.commands = {}
        self.json_handlers = []
        if os.path.exists(self.dynamic_path):
            self.json_handlers.append(JsonHandler(self, 'dynamic_commands', self.dynamic_path, ext=self.ext, commands=True, yaml=True))

    def combined(self, event, command, usercommand):
        ...

    def load(self):
        self.commands = self.static_commands

    def unload(self):
        pass

    def reload_json(self):
        """Reload any json handlers we have."""
        for json_h in self.json_handlers:
            json_h.reload()

        self.commands = self.static_commands


def isModule(member):
    if member in Module.__subclasses__():
        return True
    return False


class Modules:
    """Manages goshubot's modules."""

    def __init__(self, bot):
        self.bot = bot
        self.whole_modules = {}
        self.modules = {}
        self.paths = []

    def add_path(self, path):
        if path not in sys.path:
            self.paths.append(path)
            sys.path.insert(0, path)

    def modules_from_path(self, path):
        modules = []
        for entry in os.listdir(path):
            if os.path.isfile(os.path.join(path, entry)):
                (name, ext) = os.path.splitext(entry)
                if ext == os.extsep + 'py' and name != '__init__':
                    modules.append(name)
            elif os.path.isfile((os.path.join(path, entry, os.extsep.join(['__init__', 'py'])))):
                modules.append(entry)
        return modules

    def load_init(self, path):
        self.add_path(path)
        modules = self.modules_from_path(path)
        output = 'modules '
        for module in modules:
            loaded_module = self.load(module)
            if loaded_module:
                output += ', '.join(self.whole_modules[module]) + ', '
            else:
                output += module + '[FAILED], '
        output = output[:-2]
        output += ' loaded'
        self.bot.gui.put_line(output)

    def load(self, name):
        whole_module = importlib.import_module(name)
        imp.reload(whole_module)  # so reloading works

        # find the actual goshu Module(s) we wanna load from the whole module
        modules = []
        for item in inspect.getmembers(whole_module, isModule):
            modules.append(item[1](self.bot))
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

            module.static_commands = {}
            for command in module.events['commands']:
                self.add_command_info(module.name, command)
            module.folder_path = 'modules' + os.sep + name
            module.bot = self.bot

            module.load()

        return True

    def unload(self, name):
        if name not in self.whole_modules:
            self.bot.gui.put_line('module', name, 'not in', self.whole_modules)
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
                module_commands = self.modules[module].commands
                for search_command in ['*', command_name]:
                    if search_command in module_commands:
                        command_info = module_commands[search_command]
                        if userlevel >= command_info.call_level:
                            if command_info.call not in called:
                                called.append(command_info.call)
                                threading.Thread(target=command_info.call,
                                                 args=(event, command_info,
                                                       UserCommand(command_name, command_args))).start()
                        else:
                            self.bot.gui.put_line('        No Privs')

    def add_command_info(self, module, name):
        info = self.modules[module].events['commands'][name]

        if isinstance(name, tuple):
            self.modules[module].static_commands[name[0]] = Command(info)

            for alias in name[1:]:
                self.modules[module].static_commands[alias] = Command(info, alias=name[0])

        elif isinstance(name, str):
            self.modules[module].static_commands[name] = Command(info)

    def return_command_dict(self, base, info):
        commands = {}

        if 'call' in info:
            call = getattr(self, info['call'])
        else:
            call = base.combined

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

        commands[info['name'][0]] = Command(call=call, desc=desc, call_level=call_level,
                                            view_level=view_level, json=info)

        for command in info['name'][1:]:
            commands[command] = Command(call=call, desc=desc, call_level=call_level,
                                        view_level=view_level, json=info, alias=info['name'][0])

        return commands


class Command:
    """Goshubot command storage."""
    def __init__(self, base_info=None, **kwargs):
        if base_info:
            self.call = base_info[0]
            self.desc = base_info[1]
            if len(base_info) > 2:
                self.call_level = base_info[2]
            else:
                self.call_level = 0

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
