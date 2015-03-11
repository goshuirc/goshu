#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import os
import sys
import imp
import json
import inspect
import importlib
import threading

from .libs.helper import JsonHandler, add_path
from .libs.girclib import NickMask, is_channel
from .users import USER_LEVEL_NOPRIVS


# special custom json encoder
class IEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o.__json__()
        except:
            return o


def json_dumps(*pargs, **kwargs):
    """Special json dumper to use our __json__ function where appropriate."""
    return json.dumps(*pargs, cls=IEncoder, **kwargs)


class Module:
    """Module to add commands/functionality to the bot."""
    # whether this module is 'core', or practically required for
    #   Goshu to operate
    core = False

    def __init__(self, bot):
        self.bot = bot

        if getattr(self, 'name', None) is None:
            self.name = self.__class__.__name__

        if getattr(self, 'ext', None) is None:
            if len(self.name) >= 3:
                self.ext = self.name[:3]
            else:
                self.ext = self.name

        self.dynamic_path = os.path.join('.', 'modules', self.name)

        self.commands = {}
        self.json_handlers = []
        self.dynamic_commands = {}

        self.config = {}
        self.config_filename = os.sep.join(['config', 'modules', '{}.json'.format(self.name)])

    def load(self):
        """Actually start up everything we need"""
        if os.path.exists(self.dynamic_path):
            # setup our new module's dynamic json command handler
            new_handler = JsonHandler(self, self.dynamic_path, **{
                'attr': 'dynamic_commands',
                'callback_name': '_json_command_callback',
                'ext': self.ext,
                'yaml': True,
            })
            self.json_handlers.append(new_handler)
            self.reload_json()

        self.commands.update(getattr(self, 'static_commands', {}))

        self.load_config()

    def load_config(self, path=None):
        """Load config from our config file."""
        if path is None:
            path = self.config_filename

        try:
            with open(path, 'r', encoding='utf-8') as config_file:
                self.config = json.loads(config_file.read())
        except FileNotFoundError:
            self.config = {}

    def save_config(self, path=None):
        """Save config to our config file."""
        if path is None:
            path = self.config_filename

        with open(path, 'w', encoding='utf-8') as config_file:
            config_file.write(json_dumps(self.config, sort_keys=True, indent=4))

    def is_ignored(self, target):
        """Whether the target is ignored in our config."""
        if is_channel(target):
            return target.lower() in self.config.get('ignored', [])
        else:
            return NickMask(target).nick.lower() in self.config.get('ignored', [])

    def combined(self, event, command, usercommand):
        ...

    def unload(self):
        pass

    def reload_json(self):
        """Reload any json handlers we have."""
        for json_h in self.json_handlers:
            json_h.reload()

    def _json_command_callback(self, new_json):
        """Update our command dictionary.
        Mixes new json dynamic commands with our static ones.
        """
        # assemble new json dict into actual commands dict
        new_commands = {}
        disabled_commands = self.bot.settings.get('dynamic_commands_disabled', {}).get(self.name.lower(), [])
        for key in new_json:
            if key in disabled_commands:
                continue

            single_command_dict = self.bot.modules.return_command_dict(self, new_json[key])
            new_commands.update(single_command_dict)

        # merge new dynamic commands with static ones
        commands = getattr(self, 'static_commands', {}).copy()
        commands.update(new_commands)
        commands.update(getattr(self, 'static_commands', {}))

        self.commands = commands


def isModule(member):
    if member in Module.__subclasses__():
        return True
    return False


class Modules:
    """Manages goshubot's modules."""
    def __init__(self, bot, path):
        self.bot = bot
        self.whole_modules = {}
        self.modules = {}
        self.path = path
        add_path(path)

        # info lists
        self.core_module_names = []
        self.dcm_module_commands = {}  # dynamic command module command lists

    def load_module_info(self):
        modules = self._modules_from_path()

        # load so we can work out which modules are core and which aren't
        for mod_name in modules:
            loaded_module = self.load(mod_name)
            if self.modules[mod_name].core:
                self.core_module_names.append(mod_name)
            if self.modules[mod_name].dynamic_commands:
                self.dcm_module_commands[mod_name] = list(self.modules[mod_name].dynamic_commands.keys())
            self.unload(mod_name)

    def _modules_from_path(self, path=None):
        if path is None:
            path = self.path

        modules = []
        for entry in os.listdir(path):
            if os.path.isfile(os.path.join(path, entry)):
                (name, ext) = os.path.splitext(entry)
                if ext == os.extsep + 'py' and name != '__init__':
                    modules.append(name)
            elif os.path.isfile((os.path.join(path, entry, os.extsep.join(['__init__', 'py'])))):
                modules.append(entry)
        return modules

    def load_init(self):
        modules = self._modules_from_path()
        output = 'modules '
        for module in modules:
            loaded_module = self.load(module)
            self.modules[module].load()
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
            module.folder_path = os.path.join('modules', name)
            module.bot = self.bot

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
        if event.arguments[0].startswith(self.bot.settings.store['command_prefix']):
            in_string = event.arguments[0][len(self.bot.settings.store['command_prefix']):].strip()
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
                            # for commands restricted by channel, make and check the priv lists
                            source_chan = event.target
                            source_nick = NickMask(event.source).nick

                            current_channel_whitelist = [self.bot.irc.servers[event.server].istring(chan) for chan in command_info.channel_whitelist]
                            current_user_whitelist = []
                            for chan in current_channel_whitelist:
                                [current_user_whitelist.append(user) for user in self.bot.irc.servers[event.server].get_channel_info(chan)['users']]

                            if source_chan in current_channel_whitelist or source_nick in current_user_whitelist or (not current_channel_whitelist):
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

        if 'description' in info:
            if isinstance(info['description'], str):
                description = [info['description']]
            elif isinstance(info['description'], list):
                description = info['description']
        else:
            description = ''

        call_level = info.get('call_level', USER_LEVEL_NOPRIVS)

        if 'view_level' in info:
            view_level = info['view_level']
        else:
            view_level = call_level

        channel_whitelist = info.get('channel_whitelist', [])

        commands[info['name'][0]] = Command(call=call, description=description, call_level=call_level,
                                            view_level=view_level, channel_whitelist=channel_whitelist,
                                            json=info)

        for command in info['name'][1:]:
            commands[command] = Command(call=call, description=description, call_level=call_level,
                                        view_level=view_level, channel_whitelist=channel_whitelist,
                                        json=info, alias=info['name'][0])

        return commands


class Command:
    """Goshubot command storage."""
    def __init__(self, base_info=None, **kwargs):
        # defaults
        self.alias = False
        self.channel_whitelist = []

        # all other actual data
        if base_info:
            self.call = base_info[0]
            self.description = base_info[1]
            if len(base_info) > 2:
                self.call_level = base_info[2]
            else:
                self.call_level = USER_LEVEL_NOPRIVS

            if len(base_info) > 3:
                self.view_level = base_info[3]
            else:
                self.view_level = self.call_level

        if kwargs:
            for key in kwargs:
                setattr(self, key, kwargs[key])

        if isinstance(self.description, str):
            self.description = [self.description]


class UserCommand:
    """Command from a client."""

    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments


# command splitting for modules
def cmd_split(in_str):
    if len(in_str.split()) > 1:
        do, args = in_str.split(' ', 1)
    else:
        do = in_str
        args = ''

    do = do.lower()

    return do, args


def std_ignore_command(self, event, do, args):
    """Provides the standard 'ignore' command."""
    if do == 'list':
        target_list = ', '.join(self.config.get('ignored', []))
        if not target_list:
            target_list = 'None'

        msg = 'Ignored targets: {}'.format(target_list)
        self.bot.irc.msg(event, msg, 'private')

    elif do == 'add':
        targets = args.lower().split()

        if 'ignored' not in self.config:
            self.config['ignored'] = []

        for target in targets:
            if target not in self.config['ignored']:
                self.config['ignored'].append(target)

        self.save_config()

        msg = 'All given targets are now ignored'
        self.bot.irc.msg(event, msg, 'private')

    elif do == 'del':
        targets = args.lower().split()

        if 'ignored' not in self.config:
            self.config['ignored'] = []

        for target in targets:
            if target in self.config['ignored']:
                self.config['ignored'].remove(target)

        self.save_config()

        msg = 'All given targets are no longer ignored'
        self.bot.irc.msg(event, msg, 'private')
