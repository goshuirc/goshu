#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.users import USER_LEVEL_ADMIN, USER_LEVEL_SUPERADMIN, USER_LEVEL_OWNER


class accounts(Module):
    """Handles goshu accounts, including registration, access levels, and login."""
    core = True

    def nickserv_listener(self, event):
        """Handles incoming NickServ messages.

        @listen in privmsg high
        """
        if event.source.split('!')[0].lower() == 'nickserv':
            response = event.arguments[0].lower()
            sresponse = response.split()
            if len(sresponse) == 3 and sresponse[1] == 'is':
                self.bot.gui.put_line('Nickserv success response: {nick} is {acct}'.format(nick=sresponse[0], acct=sresponse[2]))
            elif "isn't registered" in response:
                self.bot.gui.put_line('Nickserv fail response: {nick} is not registered'.format(nick=sresponse[1]))

    def cmd_nickserv(self, event, command, usercommand):
        """Link, List, or Delete NickServ-linked bot accounts

        @usage <link/list/del>
        """
        if usercommand.arguments.lower() == 'link':
            self.bot.irc.servers[event.server].privmsg('nickserv', 'INFO {nick}'.format(nick=event.source.split('!')[0]))

    def cmd_register(self, event, command, usercommand):
        """Register a bot account

        @usage <username> <password> [email]
        """
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

    def cmd_login(self, event, command, usercommand):
        """Login to a bot account, if no user/password given try NickServ integration

        @usage [[username] [password]]
        """
        user_args = usercommand.arguments.split()

        if user_args is None:
            # Aww yeah nickserv attempt!
            ...

        elif (len(user_args) > 1) and self.bot.accounts.login(user_args[0].lower(), user_args[1], event.server, event.source):
            self.bot.irc.msg(event, 'Login accepted!')

    def cmd_loggedin(self, event, command, usercommand):
        """See if you are logged in"""
        name = self.bot.accounts.account(event.source, event.server)
        if name:
            self.bot.irc.msg(event, 'Logged into {acct}'.format(acct=name))
        else:
            self.bot.irc.msg(event, 'Not logged in')

    def cmd_owner(self, event, command, usercommand):
        """Make yourself a bot owner

        @usage <password>
        @view_level owner
        @call_level noprivs
        """
        name = self.bot.accounts.account(event.source, event.server)
        if name:
            if self.bot.settings.encrypt(usercommand.arguments) == self.bot.settings.get('master_bot_password', None):
                self.bot.accounts.set_access_level(name, USER_LEVEL_OWNER)
                self.bot.irc.msg(event, 'You are now a bot owner')

    def cmd_setaccess(self, event, command, usercommand):
        """Set user's access level

        @usage <username> [admin/superadmin/owner/0-10]
        @call_level admin
        """
        splitargs = usercommand.arguments.split()
        if len(splitargs) < 2:
            return

        # make sure user has privs
        useraccount = self.bot.accounts.account(event.source, event.server)
        if useraccount:
            accesslevel = self.bot.accounts.access_level(useraccount)
        else:
            return

        # get access level
        access_level_to_set = None
        if splitargs[1].isdecimal():
            access_level_to_set = int(splitargs[1])
        elif splitargs[1].lower() == 'admin':
            access_level_to_set = USER_LEVEL_ADMIN
        elif splitargs[1].lower() == 'superadmin':
            access_level_to_set = USER_LEVEL_SUPERADMIN
        elif splitargs[1].lower() == 'owner':
            access_level_to_set = USER_LEVEL_OWNER
        else:
            self.bot.irc.msg(event, "Don't know what that access level means. You can either use a number, or admin/superadmin/owner")
            return

        if access_level_to_set >= accesslevel and accesslevel != USER_LEVEL_OWNER:
            self.bot.irc.msg(event, 'You can only set access levels lower than your own (lower than {})'.format(accesslevel))
            return

        if splitargs[1].isdecimal() and accesslevel >= int(splitargs[1]):
            self.bot.irc.msg(event, "Setting {acct}'s access level to {level}".format(acct=splitargs[0], level=splitargs[1]))
            self.bot.accounts.set_access_level(splitargs[0], int(splitargs[1]))
