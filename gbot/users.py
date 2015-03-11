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
    version = 2

    # version upgrading
    def update_store_version(self, current_version):
        if current_version == 1:
            new_store = {
                'store_version': 2,
                'accounts': {},
            }
            for name, info in self.store.items():
                new_store['accounts'][name] = info

            self.store = new_store
            self.save()

            current_version = 2

        return current_version

    # standard menus
    def add_standard_keys(self):
        wrap = self.bot._prompt_wraps

        # module settings
        #
        print(wrap['section']('Accounts'))

        print(wrap['success']('Accounts'))

    def add_account(self, name, password):
        """Add an account to our internal list."""
        if self.account_exists(name):
            raise Exception('Given account [{}] already exists'.format(name))

        self.store['accounts'][name] = {}
        self.store['accounts'][name]['password'] = self.encrypt(password)

        self.store['accounts'][name]['modules'] = {}

        self.save()

    def remove_account(self, name):
        """Remove an account from our internal list."""
        self.load()
        if name in self.store['accounts']:
            del self.store['accounts'][name]
            self.save()
            return True
        else:
            self.save()
            return False

    def account_exists(self, name):
        self.load()
        if name in self.store['accounts']:
            return True
        else:
            return False

    def is_password(self, name, password):
        self.load()
        if self.account_exists(name):
            if self.store['accounts'][name]['password'] == self.encrypt(password):
                return True
        return False

    def set_password(self, name, password):
        self.load()
        if self.account_exists(name):
            self.store['accounts'][name]['password'] = self.encrypt(password)
            self.save()

    def login(self, name, password, server, userstring):
        self.load()
        if self.is_password(name, password):
            self.bot.irc.servers[server].create_or_update_user(userstring)
            user_nick = self.bot.irc.servers[server].istring(girclib.NickMask(userstring).nick)
            self.bot.irc.servers[server].info['users'][user_nick]['accountinfo'] = {}
            self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']['name'] = name
            self.bot.irc.servers[server].info['users'][user_nick]['accountinfo']['userhost'] = girclib.NickMask(userstring).userhost
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
            self.store['accounts'][name]['level'] = level
            if level == 0:
                del self.store['accounts'][name]['level']
            self.save()
            return True
        return False

    def access_level(self, name):
        self.load()
        level = USER_LEVEL_NOPRIVS
        if self.account_exists(name):
            if 'level' in self.store['accounts'][name]:
                level = self.store['accounts'][name]['level']
        return level

    def online_bot_runners(self, server):
        """Returns a list of the currently online owners, superadmins/admins, or none."""
        privs = {}
        user_info = dict(self.bot.irc.servers[server].info['users'])
        for user_nick in user_info:
            if 'accountinfo' in user_info[user_nick]:
                access_level = self.access_level(user_info[user_nick]['accountinfo']['name'])
                if access_level >= USER_LEVEL_ADMIN:
                    if access_level not in privs:
                        privs[access_level] = []
                    privs[access_level].append(user_nick)

        if privs:
            max_priv_level = sorted(privs)[-1]
            return max_priv_level, privs[max_priv_level]

        return 0, []
