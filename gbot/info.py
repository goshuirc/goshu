#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license
import hashlib
import json
import codecs
import os

from colorama import Fore, Back, Style

from .libs import helper


class InfoStore():
    """Stores and manages general information, settings, etc; to be subclassed."""
    def __init__(self, bot, path):
        self.bot = bot
        self.path = path
        self.store = {}
        self.load()

    # loading and saving
    def load(self):
        """Load information from our data file."""
        try:
            with open(self.path, 'r') as info_file:
                self.store = json.loads(info_file.read())
        except FileNotFoundError:
            self.store = {}

    def save(self):
        """Save information to our data file."""
        with open(self.path, 'w') as info_file:
            info_file.write(json.dumps(self.store, sort_keys=True, indent=4))

    # getting and setting
    def has_key(self, key):
        """Returns True if we have the given key in our store."""
        return key in self.store

    def has_all_keys(self, *keys):
        """Returns True if we have all of the given keys in our store."""
        for key in keys:
            if not self.has_key(key):
                return False
        return True

    def set(self, key, value):
        """Sets key to value in our store."""
        self.store[key] = value
        self.save()

    def get(self, key, default=None):
        """Returns value from our store, or default if it doesn't exist."""
        return self.store.get(key, default)

    def remove(self, key):
        """Remove the given key from our store."""
        if self.has_key(key):
            del self.store[key]
            self.save()

    # complex junk
    def add_key(self, value_type, key, prompt, repeating_prompt=None, confirm_prompt=None, 
                default=None, allow_none=False, blank_allowed=False, password=False,
                encrypted=False):
        """Adds given key to our store, and requests it if not yet defined.

        Args:
            value_type: type of value (eg: str, int, float)
            key: key name to store it as
            prompt: what to prompt the user with if it does not exist
            repeating_prompt: prompt on repeated question, defaults to prompt
            confirm_prompt: (str) prompt to confirm the value, prompts for value twice if given
            default: if defined, set this if the user does not type in a value themselves
            password: use a password prompt, that does not echo characters typed for the value
            allow_none: allow the default value `None` for bool keys
            blank_allowed: allow a blank string when requesting string value from the user
            encrypted: (str) store it encrypted blob in our store
        """
        if self.has_key(key):
            return

        if repeating_prompt is None:
            repeating_prompt = prompt

        if value_type == str:
            if default is not None:
                blank_allowed = True

            value = self.bot.gui.get_string(prompt, repeating_prompt=repeating_prompt, confirm_prompt=confirm_prompt, blank_allowed=blank_allowed, password=password)

            if default is not None and value.strip() == '':
                value = default

            if encrypted:
                value = self.encrypt(value)
        elif value_type == float:
            value = self.bot.gui.get_number(prompt, repeating_prompt=repeating_prompt, default=default, password=password)
        elif value_type == int:
            value = self.bot.gui.get_number(prompt, repeating_prompt=repeating_prompt, default=default, force_int=True, password=password)
        elif value_type == bool:
            value = self.bot.gui.get_bool(prompt, repeating_prompt=repeating_prompt, default=default, allow_none=allow_none, password=password)
        else:
            raise Exception('Unknown value_type {} in InfoStore[{}]'.format(value_type, self))

        self.set(key, value)

    # misc
    def encrypt(self, password):
        """Returns hashed password."""
        if type(password) == str:
            password = password.encode()
        return hashlib.sha512(password).hexdigest()

    def add_standard_keys(self):
        """Add custom keys."""
        pass


class BotSettings(InfoStore):
    """Manages basic bot settings."""
    def add_standard_keys(self):
        wrap = self.bot._prompt_wraps

        # module settings
        #
        print(wrap['section']('Modules'))

        # core modules
        repeating_prompt = wrap['prompt']('Load all core modules? [yes]')
        prompt = '\n'.join([
            wrap['subsection']('Core Modules'),
            "Core modules provide the core functionality and commands required for running "
            "and administering your bot.",
            '',
            "You should leave this enabled unless you're reprogramming the Goshu internals.",
            '',
            repeating_prompt,
        ])
        self.add_key(bool, 'load_all_core_modules', prompt, repeating_prompt=repeating_prompt, default=True)

        if not self.get('load_all_core_modules'):
            enabled = self.get('core_modules_enabled', [])
            disabled = self.get('core_modules_disabled', [])

            for module in self.bot.modules.all_core_modules():
                module_slug = module.name.lower()
                if module_slut not in enabled and module_slug not in disabled:
                    prompt = wrap['prompt']('Load core module {}: [y]'.format(module.name))
                    enable_module = self.bot.gui.get_bool(prompt, default=True)

                    if enable_module:
                        enabled.append(module_slug)
                    else:
                        disabled.append(module_slug)

            self.set('core_modules_enabled', enabled)
            self.set('core_modules_disabled', disabled)

        # dynamic command modules
        repeating_prompt = wrap['prompt']('Load all dynamic command modules? [yes]')
        prompt = '\n'.join([
            wrap['subsection']('Dynamic Command Modules'),
            "Dynamic command modules provide commands based off JSON and YAML files in the "
            "module's folder. This lets you create a site-specific Google search command or "
            "a command that queries and returns results from a site's API without programming "
            "your own module, instead simply creating a simple JSON file to do so.",
            '',
            wrap['note']("Disabling this will prevent Youtube, Google, Gelbooru, Wikipedia, "
                "and the standard 'responses' commands."),
            wrap['note']("If you want to disable just specific commands, you'll be able to "
                "run through and disable them one-by-one instead in a moment."),
            '',
            "You should leave this enabled unless you know what you're doing.",
            '',
            repeating_prompt,
        ])
        self.add_key(bool, 'load_all_dynamic_command_modules', prompt, repeating_prompt=repeating_prompt, default=True)

        repeating_prompt = wrap['prompt']('Run through existing dynamic commands one-by-one '
            'and approve / disable them? [no]')
        prompt = '\n'.join([
            wrap['subsection']('Dynamic Commands'),
            "Dynamic commands are specific commands, such as 'gel for searching Gelbooru, "
            "'youtube for searching Youtube, 'imgur for searching Imgur, etc.",
            '',
            "Here you may disable them one-by-one, so you are left with just the ones you "
            "prefer for your own channel / network.",
            '',
            wrap['note']("Enabling this means you will be asked about newly-added dynamic "
                "commands every time the bot is started."),
            wrap['note']("You may also disable commands while the bot is running through the "
                "  'module commands   command."),
            '',
            repeating_prompt,
        ])
        self.add_key(bool, 'confirm_all_dynamic_commands', prompt, repeating_prompt=repeating_prompt, default=False)

        print(wrap['success']('Modules'))

        # bot control settings
        #
        print(wrap['section']('Bot Control'))

        repeating_prompt = wrap['prompt']('Default Nick:')
        prompt = '\n'.join([
            wrap['subsection']('Default Nick'),
            "This will be the default nick your bot uses for new networks. You may also set a "
            "custom nick on each network, this will just be the default choice.",
            '',
            repeating_prompt,
        ])
        self.add_key(str, 'default_nick', prompt, repeating_prompt=repeating_prompt)

        repeating_prompt = wrap['prompt']("Command prefix: [']")
        prompt = '\n'.join([
            wrap['subsection']('Command Prefix'),
            "Users will need to type this before every command to use it. For instance:",
            "  .google Puppies and Kittens",
            "  'google Puppies and Kittens",
            "  !google Puppies and Kittens",
            '',
            "The recommended (and default) command prefix is ' , as this is not widely-"
            "spread, should not cause any conflicts, and is simple to type.",
            '',
            wrap['note'](". is commonly the services (ChanServ) default command prefix, so we "
                "do not recommend using it."),
            '',
            repeating_prompt,
        ])
        self.add_key(str, 'command_prefix', prompt, repeating_prompt=repeating_prompt, default="'")

        repeating_prompt = wrap['prompt']('Master Bot Password:')
        confirm_prompt = wrap['prompt']('Confirm Master Bot Password:')
        prompt = '\n'.join([
            wrap['subsection']('Master Bot Password'),
            "This password controls master access to the bot, and anyone with this password "
            "can access ANY function, run ANY command, and have complete control over your bot."
            '',
            "Needless to say, try to make it something long, difficult to guess, and memorable.",
            '',
            repeating_prompt,
        ])
        self.add_key(str, 'master_bot_password', prompt, repeating_prompt=repeating_prompt, confirm_prompt=confirm_prompt, password=True, encrypted=True)

        print(wrap['success']('Bot Control'))


class IrcInfo(InfoStore):
    """Manages bot's IRC info."""
    def add_standard_keys(self):
        wrap = self.bot._prompt_wraps

        # module settings
        #
        print(wrap['section']('IRC Info'))

        if self.has('servers'):
            repeating_prompt = wrap['prompt']('Current IRC connections OK? [y]')
            prompt = '\n'.join([
                wrap['subsection']('Current IRC Connections'),
                "If you wish to edit the current IRC connections, type 'no' here.",
                '',
                repeating_prompt,
            ])
            modify_connections = self.bot.gui.get_bool(prompt, repeating_prompt=repeating_prompt, default=True)

            # remove connections
            if modify_connections:
                current_servers = self.get('servers', {})
                for name in current_servers:
                    server_info = current_servers[name]
                    prompt = wrap['prompt']('Delete Server {name} [{ssl}{addr}:{port}] [n]'.format(**{
                        'name': name,
                        'ssl': '+' if server_info['ssl'] else '',
                        'addr': server_info['address'],
                        'port': server_info['port'],
                    }))
                    delete_server = self.bot.gui.get_bool(prompt, default=False)

                    if delete_server:
                        del current_servers[name]

                self.set('servers', current_servers)

            # new connections
            header = '\n'.join([
                wrap['subsection']('New IRC Connections'),
            ])
            print(header)

            while True:
                if not self.has('servers') or not self.get('servers', None):
                    new_connection = True
                else:
                    prompt = wrap['prompt']('Add new server? [n]')
                    setup_new_connection = self.bot.gui.get_bool(prompt, default=False)

                    if not setup_new_connection
                        break

                # setup new connection
                if setup_new_connection:
                    new_connection = {}

                    prompt = wrap['prompt']('Server Nickname:')
                    server_name = self.bot.gui.get_string(prompt)

                    prompt = wrap['prompt']('Hostname:')
                    new_connection['hostname'] = self.bot.gui.get_string(prompt)

                    prompt = wrap['prompt']('IPv6?')
                    new_connection['ipv6'] = self.bot.gui.get_bool(prompt)

                    prompt = wrap['prompt']('SSL?')
                    new_connection['ssl'] = self.bot.gui.get_bool(prompt)

                    if new_connection['ssl']:
                        default_port = 6697
                    else:
                        default_port = 6667

                    prompt = wrap['prompt']('Port? [{}]'.format(default_port))
                    new_connection['port'] = self.bot.gui.get_number(prompt, force_int=True, default=default_port)

                    print(wrap['note']('If you do not have a NickServ password, simply hit enter here'))
                    prompt = wrap['prompt']('NickServ Password:')
                    new_connection['nickserv_password'] = self.bot.gui.get_string(prompt, password=True)

                    if new_connection['nickserv_password']:
                        prompt = wrap['prompt']('NickServ Wait Period')




#         if server:
#             new_server_name = ''
#             while new_server_name == '':
#                 try:
#                     new_server_name = self.bot.gui.get_input(' server nickname [%s]: ' % server).split()[0].strip()
#                 except IndexError:
#                     new_server_name = server
#         else:
#             new_server_name = ''
#             while new_server_name == '':
#                 try:
#                     new_server_name = self.bot.gui.get_input(' server nickname: ').split()[0].strip()
#                 except IndexError:
#                     new_server_name = ''

#         new_server['connection'] = {}
#         self._update_attribute(old_server, new_server, 'connection.address', 'server address')
#         self._update_attribute(old_server, new_server, 'connection.ipv6', 'ipv6', truefalse=True, no_old_value=False)
#         self._update_attribute(old_server, new_server, 'connection.ssl', 'ssl', truefalse=True, no_old_value=False)
#         if new_server['connection']['ssl']:
#             assumed_port = 6697
#         else:
#             assumed_port = 6667
#         self._update_attribute(old_server, new_server, 'connection.port', 'port', old_value=assumed_port)
#         self._update_attribute(old_server, new_server, 'connection.nickserv_password', 'nickserv password', can_ignore=True)

#         store[new_server_name] = new_server

#         return True















# class IrcInfo(InfoStore):
#     """Manages goshubot IRC info."""

#     name = 'IrcInfo'

#     def update(self):
#         """Make sure servers are correct, etc."""
#         old_store = self.store
#         new_store = {}

#         if len(old_store) < 1:
#             self._update_server(new_store, None)

#         for server in old_store.copy():
#             prompt = ' '
#             prompt += server + ' '
#             prompt += old_store[server]['connection']['address'] + ':'
#             prompt += str(old_store[server]['connection']['port']) + ' '
#             if 'ssl' in old_store[server]['connection'] and old_store[server]['connection']['ssl'] is True:
#                 prompt += 'ssl '
#             if 'ipv6' in old_store[server]['connection'] and old_store[server]['connection']['ipv6'] is True:
#                 prompt += 'ipv6 '
#             prompt += '- ok? [y]: '
#             if helper.is_ok(self.bot.gui.get_input, prompt, True, True):
#                 new_store[server] = old_store[server]
#             else:
#                 if self._update_server(old_store, server):
#                     new_store[server] = old_store[server]

#         self.store = new_store

#     def _update_server(self, store, server):
#         if server:
#             old_server = store[server]
#             del store[server]
#             if helper.is_ok(self.bot.gui.get_input, ' delete server? [n]: ', False, True):
#                 return False
#         else:
#             old_server = {}
#         new_server = {}

#         if server:
#             new_server_name = ''
#             while new_server_name == '':
#                 try:
#                     new_server_name = self.bot.gui.get_input(' server nickname [%s]: ' % server).split()[0].strip()
#                 except IndexError:
#                     new_server_name = server
#         else:
#             new_server_name = ''
#             while new_server_name == '':
#                 try:
#                     new_server_name = self.bot.gui.get_input(' server nickname: ').split()[0].strip()
#                 except IndexError:
#                     new_server_name = ''

#         new_server['connection'] = {}
#         self._update_attribute(old_server, new_server, 'connection.address', 'server address')
#         self._update_attribute(old_server, new_server, 'connection.ipv6', 'ipv6', truefalse=True, no_old_value=False)
#         self._update_attribute(old_server, new_server, 'connection.ssl', 'ssl', truefalse=True, no_old_value=False)
#         if new_server['connection']['ssl']:
#             assumed_port = 6697
#         else:
#             assumed_port = 6667
#         self._update_attribute(old_server, new_server, 'connection.port', 'port', old_value=assumed_port)
#         self._update_attribute(old_server, new_server, 'connection.nickserv_password', 'nickserv password', can_ignore=True)

#         store[new_server_name] = new_server

#         return True

#     def _update_attribute(self, old_server, new_server, attribute, display_name, old_value=None, truefalse=False, can_ignore=False, no_old_value=None):
#         attribute = attribute.split('.')
#         (paths, attribute_name) = (attribute[:-1], attribute[-1])

#         if not old_value:
#             try:
#                 old_path = old_server
#                 for path in paths:
#                     old_path = old_path[path]
#                 old_value = str(old_path[attribute_name])
#             except KeyError:
#                 old_value = None

#         if old_value is None:
#             if no_old_value:
#                 old_value = True
#             elif no_old_value is False:
#                 old_value = False

#         if old_value is not None:
#             if truefalse:
#                 new_value = helper.is_ok(self.bot.gui.get_input, '    %s [%s]: ' % (display_name, str(old_value)), old_value, True)
#             else:
#                 new_value = self.bot.gui.get_input('  %s [%s]: ' % (display_name, str(old_value))).strip()
#             if new_value == '':
#                 new_value = old_value
#         else:
#             new_value = ''
#             while new_value == '':
#                 try:
#                     if truefalse:
#                         new_value = helper.is_ok(self.bot.gui.get_input, '    %s: ' % display_name, '', True)
#                     else:
#                         new_value = self.bot.gui.get_input('  %s: ' % display_name).strip()
#                 except IndexError:
#                     if can_ignore:
#                         new_value = None
#                     else:
#                         new_value = ''

#         new_path = new_server
#         for path in paths:
#             new_path = new_path[path]
#         if new_value is not None:
#             new_path[attribute_name] = new_value


# class BotSettings(InfoStore):
#     """Manages goshubot settings."""

#     name = 'BotSettings'

#     def update(self):
#         """Update the current data file."""
#         old_store = self.store
#         new_store = {}

#         new_store['nick'] = self._update_attribute('nick', old_store)
#         new_store['passhash'] = self._update_attribute('passhash', old_store, password=True, display_name='password')
#         new_store['prefix'] = self._update_attribute('prefix', old_store, display_name='bot command prefix')

#         self.store = new_store

#     def _update_attribute(self, name, store, password=False, display_name=None):
#         """Return updated single piece of data."""
#         if display_name is None:
#             display_name = name
#         if password:
#             try:
#                 old_data = store[name]
#                 if password:
#                     new_data = self.bot.gui.get_input(' %s [*****]: ' % display_name, password=True).strip()
#                     if new_data != '':
#                         return self.encrypt(new_data.encode('utf8'))
#                     else:
#                         return old_data
#             except KeyError:
#                 data = ''
#                 while data == '':
#                     data = self.bot.gui.get_input(' %s: ' % display_name, password=password).strip()
#                 return self.encrypt(data.split()[0].encode('utf8'))

#         else:
#             try:
#                 old_data = store[name]
#                 new_data = self.bot.gui.get_input(' %s [%s]: ' % (display_name, old_data)).strip()
#                 if new_data != '':
#                     return new_data
#                 else:
#                     return old_data
#             except KeyError:
#                 data = ''
#                 while data == '':
#                     data = self.bot.gui.get_input(' %s: ' % display_name).strip()
#                 return data.split()[0]
