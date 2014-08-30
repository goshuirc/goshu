#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module


class accounts(Module):
    """Handles goshu accounts, including registration, access levels, and login."""
    name = 'accounts'

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'register': [self.register, '<username> <password> [email] --- register a goshu account'],
                'login': [self.login, '[[username] [password]] --- login to a goshu account, if no user/pass use nickserv integration'],
                'loggedin': [self.loggedin, '--- see if you are logged in'],
                'owner': [self.owner, '<password> --- make yourself a bot owner', 0, 10],
                'setaccess': [self.setaccess, "<username> <level> --- set user's access level", 1],
                'nickserv': [self.nickserv, "<link/list/del> --- link, list, or delete nickserv-goshu accounts"],
            },
            'in': {
                'privnotice': [(-30, self.nickserv_listener)],
            },
        }

    def nickserv(self, event, command, usercommand):
        if usercommand.arguments.lower() == 'link':
            self.bot.irc.servers[event.server].privmsg('nickserv', 'INFO {nick}'.format(nick=event.source.split('!')[0]))

    def nickserv_listener(self, event):
        if event.source.split('!')[0].lower() == 'nickserv':
            response = event.arguments[0].lower()
            sresponse = response.split()
            if len(sresponse) == 3 and sresponse[1] == 'is':
                self.bot.gui.put_line('Nickserv success response: {nick} is {acct}'.format(nick=sresponse[0], acct=sresponse[2]))
            elif "isn't registered" in response:
                self.bot.gui.put_line('Nickserv fail response: {nick} is not registered'.format(nick=sresponse[1]))

    def register(self, event, command, usercommand):
        user_args = usercommand.arguments.split()

        if len(user_args) < 2:
            return

        if self.bot.accounts.account_exists(user_args[0].lower()):
            self.bot.irc.msg(event, 'Sorry, that name is already registered')
            return

        self.bot.accounts.add_account(user_args[0].lower(), user_args[1])

        # if len(user_args) > 2:
        #     self.bot.accounts.store[user_args[0].lower()]['email'] = user_args[2]

        self.bot.irc.msg(event, 'Account registered!')

    def login(self, event, command, usercommand):
        user_args = usercommand.arguments.split()

        if user_args is None:
            # Aww yeah nickserv attempt!
            ...

        elif (len(user_args) > 1) and self.bot.accounts.login(user_args[0].lower(), user_args[1], event.server, event.source):
            self.bot.irc.msg(event, 'Login accepted!')

    def loggedin(self, event, command, usercommand):
        name = self.bot.accounts.account(event.source, event.server)
        if name:
            self.bot.irc.msg(event, 'Logged into {acct}'.format(acct=name))
        else:
            self.bot.irc.msg(event, 'Not logged in')

    def owner(self, event, command, usercommand):
        name = self.bot.accounts.account(event.source, event.server)
        if name:
            if self.bot.settings._encrypt(usercommand.arguments) == self.bot.settings.store['passhash']:
                self.bot.accounts.set_access_level(name, 10)
                self.bot.irc.msg(event, 'You are now a bot owner')

    def setaccess(self, event, command, usercommand):
        splitargs = usercommand.arguments.split()
        if len(splitargs) < 2:
            return

        useraccount = self.bot.accounts.account(event.source, event.server)
        if useraccount:
            accesslevel = self.bot.accounts.access_level(useraccount)
        else:
            return

        if splitargs[1].isdecimal() and accesslevel >= int(splitargs[1]):
            self.bot.irc.msg(event, "Setting {acct}'s Access Level to {level}".format(acct=splitargs[0], level=splitargs[1]))
            self.bot.accounts.set_access_level(splitargs[0], int(splitargs[1]))
