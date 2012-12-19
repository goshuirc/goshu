#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module

class accounts(Module):
    name = 'accounts'

    def __init__(self):
        self.events = {
            'commands' : {
                'register' : [self.register, '<username> <password> [email] --- register a goshu account', 0],
                'login' : [self.login, '[[username] [password]] --- login to a goshu account, if no user/pass use nickserv integration', 0],
                'loggedin' : [self.loggedin, '--- see if you are logged in', 0],
                'owner' : [self.owner, '<password> --- make yourself a bot owner', 0, 10],
                'setaccess' : [self.setaccess, "<username> <level> --- set user's access level", 1],
                'nickserv' : [self.nickserv, "<link/list/del> --- link, list, or delete nickserv-goshu accounts", 0]
            },
            'in' : {
                'notice' : [(-30, self.nickserv_listener)],
            },
        }


    def nickserv(self, event, command):
        ...

    def nickserv_listener(self, event):
        #self.bot.irc.servers[event.server].privmsg('nickserv', 'info '+event.arguments[0].split()[0])
        self.bot.curses.pad_addline('/msg nickserv info '+event.arguments[0].split()[0])

    def register(self, event, command):
        user_args = command.arguments.split()

        if len(user_args) < 2:
            return

        if self.bot.accounts.account_exists(command.arguments.split()[0].lower()):
            self.bot.irc.msg(event, 'Sorry, that name is already registered')
            return

        self.bot.accounts.add_account(user_args[0].lower(), user_args[1])

        #if len(user_args) > 2:
        #    self.bot.accounts.store[user_args[0].lower()]['email'] = user_args[2]

        self.bot.irc.msg(event, 'Account registered!')

    def login(self, event, command):
        user_args = command.arguments.split()

        if user_args is None:
            # Aww yeah nickserv attempt!
            ...

        elif (len(user_args) > 1) and self.bot.accounts.login(user_args[0].lower(), user_args[1], event.server, event.source):
            self.bot.irc.msg(event, 'Login accepted!')

    def loggedin(self, event, command):
        name = self.bot.accounts.account(event.source, event.server)
        if name:
            self.bot.irc.msg(event, 'Logged into ' + name)

    def owner(self, event, command):
        name = self.bot.accounts.account(event.source, event.server)
        if name:
            if self.bot.settings._encrypt(command.arguments) == self.bot.settings.store['passhash']:
                self.bot.accounts.set_access_level(name, 10)
                self.bot.irc.msg(event, 'You are now a bot owner')

    def setaccess(self, event, command):
        splitargs = command.arguments.split()
        if len(splitargs) < 2:
            return

        useraccount = self.bot.accounts.account(event.source, event.server)
        if useraccount:
            accesslevel = self.bot.accounts.access_level(useraccount)
        else:
            return

        if splitargs[1].isdecimal() and accesslevel >= int(splitargs[1]):
            self.bot.irc.msg(event, 'Setting ' + splitargs[0] + "'s Access Level to " + splitargs[1])
            self.bot.accounts.set_access_level(splitargs[0], int(splitargs[1]))
