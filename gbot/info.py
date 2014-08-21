#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from .libs import helper
import hashlib
import json
import codecs
import os


class Manager():
    """Manages info/settings; to be subclassed."""

    name = 'Manager'

    def __init__(self, bot, path=None):
        self.bot = bot
        self.path = path
        self.store = {}

    def ret(self, paths, store=None):
        if store:
            value = store
        else:
            value = self.store
        paths = paths.split('.')
        for path in paths:
            value = value[path]
        return value

    def use_file(self, path, load=True, update=False):
        """Sets the storage file to use."""
        self.path = path

        if load:
            try:
                self.load()
            except IOError:
                self.save()

        if update:
            self.update()

        self.save()  # make sure we can save to the file

    def load(self, path=None):
        """Load data file from `path`, or `self.path`."""
        if path:
            file = codecs.open(path, 'r', 'utf8')
            try:
                self.store = json.loads(file.read())
            except ValueError:
                self.store = {}
            file.close()
        elif self.path:
            file = codecs.open(self.path, 'r', 'utf8')
            try:
                self.store = json.loads(file.read())
            except ValueError:
                self.store = {}
            file.close()
        else:
            self.store = {}
            if self.bot.DEBUG:
                self.bot.gui.put_line(self.name+'.load : no path to load from')

    def save(self, path=None):
        """Save `self.store` in file at `path`, or `self.path`."""
        if path:
            save_path = path
        elif self.path:
            save_path = self.path
        else:
            if self.bot.DEBUG:
                self.bot.gui.put_line(self.name+'.save : no path to save to')
            return

        save_dir = save_path.rsplit(os.sep, 1)[0]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        file = open(save_path, 'w')
        file.write(json.dumps(self.store, sort_keys=True, indent=4))
        file.close()

    def update(self):
        """Update the current data file, to be overwritten by subclass."""
        ...

    def _encrypt(self, password):
        """Returns hashed password."""
        if type(password) == str:
            password = password.encode()
        return hashlib.sha512(password).hexdigest()


class Info(Manager):
    """Manages goshubot IRC info."""

    name = 'Info'

    def update(self):
        """Make sure servers are correct, etc."""
        old_store = self.store
        new_store = {}

        if len(old_store) < 1:
            self._update_server(new_store, None)

        for server in old_store.copy():
            prompt = ' '
            prompt += server + ' '
            prompt += old_store[server]['connection']['address'] + ':'
            prompt += str(old_store[server]['connection']['port']) + ' '
            if 'ssl' in old_store[server]['connection'] and old_store[server]['connection']['ssl'] == True:
                prompt += 'ssl '
            if 'ipv6' in old_store[server]['connection'] and old_store[server]['connection']['ipv6'] == True:
                prompt += 'ipv6 '
            prompt += '- ok? [y]: '
            if helper.is_ok(self.bot.gui.get_input, prompt, True, True):
                new_store[server] = old_store[server]
            else:
                if self._update_server(old_store, server):
                    new_store[server] = old_store[server]

        self.store = new_store

    def _update_server(self, store, server):
        if server:
            old_server = store[server]
            del store[server]
            if helper.is_ok(self.bot.gui.get_input, ' delete server? [n]: ', False, True):
                return False
        else:
            old_server = {}
        new_server = {}

        if server:
            new_server_name = ''
            while new_server_name == '':
                try:
                    new_server_name = self.bot.gui.get_input(' server nickname [%s]: ' % server).split()[0].strip()
                except IndexError:
                    new_server_name = server
        else:
            new_server_name = ''
            while new_server_name == '':
                try:
                    new_server_name = self.bot.gui.get_input(' server nickname: ').split()[0].strip()
                except IndexError:
                    new_server_name = ''

        new_server['connection'] = {}
        self._update_attribute(old_server, new_server, 'connection.address', 'server address')
        self._update_attribute(old_server, new_server, 'connection.ipv6', 'ipv6', truefalse=True, no_old_value=False)
        self._update_attribute(old_server, new_server, 'connection.ssl', 'ssl', truefalse=True, no_old_value=False)
        if new_server['connection']['ssl']:
            assumed_port = 6697
        else:
            assumed_port = 6667
        self._update_attribute(old_server, new_server, 'connection.port', 'port', old_value=assumed_port)
        self._update_attribute(old_server, new_server, 'connection.nickserv_password', 'nickserv password', can_ignore=True)

        store[new_server_name] = new_server

        return True

    def _update_attribute(self, old_server, new_server, attribute, display_name, old_value=None, truefalse=False, can_ignore=False, no_old_value=None):
        attribute = attribute.split('.')
        (paths, attribute_name) = (attribute[:-1], attribute[-1])

        if not old_value:
            try:
                old_path = old_server
                for path in paths:
                    old_path = old_path[path]
                old_value = str(old_path[attribute_name])
            except KeyError:
                old_value = None

        if old_value == None:
            if no_old_value:
                old_value = True
            elif no_old_value == False:
                old_value = False

        if old_value != None:
            if truefalse:
                new_value = helper.is_ok(self.bot.gui.get_input, '    %s [%s]: ' % (display_name, str(old_value)), old_value, True)
            else:
                new_value = self.bot.gui.get_input('  %s [%s]: ' % (display_name, str(old_value))).strip()
            if new_value == '':
                new_value = old_value
        else:
            new_value = ''
            while new_value == '':
                try:
                    if truefalse:
                        new_value = helper.is_ok(self.bot.gui.get_input, '    %s: ' % display_name, '', True)
                    else:
                        new_value = self.bot.gui.get_input('  %s: ' % display_name).strip()
                except IndexError:
                    if can_ignore:
                        new_value = None
                    else:
                        new_value = ''

        new_path = new_server
        for path in paths:
            new_path = new_path[path]
        if new_value != None:
            new_path[attribute_name] = new_value


class Settings(Manager):
    """Manages goshubot settings."""

    name = 'Settings'

    def update(self):
        """Update the current data file."""
        old_store = self.store
        new_store = {}

        new_store['nick'] = self._update_attribute('nick', old_store)
        new_store['passhash'] = self._update_attribute('passhash', old_store, password=True, display_name='password')
        new_store['prefix'] = self._update_attribute('prefix', old_store, display_name='bot command prefix')

        self.store = new_store

    def _update_attribute(self, name, store, password=False, display_name=None):
        """Return updated single piece of data."""
        if display_name is None:
            display_name = name
        if password:
            try:
                old_data = store[name]
                if password:
                    new_data = self.bot.gui.get_input(' %s [*****]: ' % display_name, password=True).strip()
                    if new_data != '':
                        return self._encrypt(new_data.encode('utf8'))
                    else:
                        return old_data
            except KeyError:
                data = ''
                while data == '':
                    data = self.bot.gui.get_input(' %s: ' % display_name, password=password).strip()
                return self._encrypt(data.split()[0].encode('utf8'))

        else:
            try:
                old_data = store[name]
                new_data = self.bot.gui.get_input(' %s [%s]: ' % (display_name, old_data)).strip()
                if new_data != '':
                    return new_data
                else:
                    return old_data
            except KeyError:
                data = ''
                while data == '':
                    data = self.bot.gui.get_input(' %s: ' % display_name).strip()
                return data.split()[0]


class Accounts(Manager):
    """Manages Goshubot Account Info."""

    name = 'Accounts'

    def add_account(self, name, password):
        self.store[name] = {}
        self.store[name]['password'] = self._encrypt(password)

        self.store[name]['modules'] = {}

        self.save()

    def remove_account(self, name):
        self.load()
        if name in self.store:
            del self.store[name]
            self.save()
            return True
        else:
            self.save()
            return False

    def account_exists(self, name):
        self.load()
        if name in self.store:
            return True
        else:
            return False

    def is_password(self, name, password):
        self.load()
        if self.account_exists(name):
            if self.store[name]['password'] == self._encrypt(password):
                return True
        return False

    def set_password(self, name, password):
        self.load()
        if self.account_exists(name):
            self.store[name]['password'] = self._encrypt(password)
            self.save()

    def login(self, name, password, server, userstring):
        self.load()
        if self.is_password(name, password):
            if userstring.split('!')[0] not in self.bot.irc.servers[server].info['users']:
                self.bot.irc.servers[server].create_user(userstring)
            self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]['accountinfo'] = {}
            self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]['accountinfo']['name'] = name
            self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]['accountinfo']['userhost'] = userstring.split('!')[1]
            return True
        else:
            return False

    def account(self, userstring, server):
        self.load()
        if userstring.split('!')[0] in self.bot.irc.servers[server].info['users']:
            if 'accountinfo' in self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]:
                if 'userhost' in self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]['accountinfo']:
                    if self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]['accountinfo']['userhost'] == userstring.split('!')[1]:
                        return self.bot.irc.servers[server].info['users'][userstring.split('!')[0]]['accountinfo']['name']
        return None

    def set_access_level(self, name, level=0):
        if self.account_exists(name):
            self.store[name]['level'] = level
            if level == 0:
                del self.store[name]['level']
            self.save()
            return True
        return False

    def access_level(self, name):
        self.load()
        level = 0
        if self.account_exists(name):
            if 'level' in self.store[name]:
                level = self.store[name]['level']
        return level
