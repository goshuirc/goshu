#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from .info import InfoStore
from .libs import girclib

USER_LEVEL_NOPRIVS = 0
USER_LEVEL_ADMIN = 5
USER_LEVEL_SUPERADMIN = 7
USER_LEVEL_OWNER = 10


class AccountInfo(InfoStore):
    """Manages and stores user account information."""
    name = 'Accounts'

    def add_account(self, name, password):
        """Add an account to our internal list."""
        self.store[name] = {}
        self.store[name]['password'] = self.encrypt(password)

        self.store[name]['modules'] = {}

        self.save()

    def remove_account(self, name):
        """Remove an account from our internal list."""
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
            if self.store[name]['password'] == self.encrypt(password):
                return True
        return False

    def set_password(self, name, password):
        self.load()
        if self.account_exists(name):
            self.store[name]['password'] = self.encrypt(password)
            self.save()

    def login(self, name, password, server, userstring):
        self.load()
        if self.is_password(name, password):
            self.bot.irc.servers[server].create_user(userstring)
            user_nick = self.bot.irc.servers[server].istring(girclib.NickMask(userstring).nick)
            self.bot.irc.servers[server].info['users'][user_nick]['accountinfo'] = {}
            self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']['name'] = name
            self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']['userhost'] = userstring.split('!')[1]
            return True
        else:
            return False

    def account(self, userstring, server):
        self.load()
        user_nick = self.bot.irc.servers[server].istring(girclib.NickMask(userstring).nick)
        if user_nick in self.bot.irc.servers[server].info['users']:
            if 'accountinfo' in self.bot.irc.servers[server].info['users'][user_nick]:
                if 'userhost' in self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']:
                    if self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']['userhost'] == userstring.split('!')[1]:
                        return self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']['name']
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
        level = USER_LEVEL_NOPRIVS
        if self.account_exists(name):
            if 'level' in self.store[name]:
                level = self.store[name]['level']
        return level
