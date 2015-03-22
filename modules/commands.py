#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.helper import split_num
from gbot.users import USER_LEVEL_ADMIN, USER_LEVEL_SUPERADMIN


class commands(Module):
    """Provides general IRC commands such as msg, me, join, part."""
    core = True

    # irc
    def cmd_msg(self, event, command, usercommand):
        """Send a /msg

        @usage <target> <message>
        @call_level admin
        """
        msg_target, msg_msg = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].privmsg(msg_target, msg_msg)

    def cmd_me(self, event, command, usercommand):
        """Send a /me

        @usage <target> <message>
        @call_level admin
        """
        msg_target, msg_msg = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].action(msg_target, msg_msg)

    def cmd_join(self, event, command, usercommand):
        """Join a channel

        @usage <channel>
        @call_level admin
        """
        channel, key = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].join(channel, key)

    def cmd_part(self, event, command, usercommand):
        """Leave a channel

        @usage <channel>
        @call_level admin
        """
        channel, reason = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].part(channel, reason)

    # goshu control
    def cmd_shutdown(self, event, command, usercommand):
        """Shutdown bot

        @usage [quit message]
        @call_level superadmin
        """
        message = usercommand.arguments
        self.bot.irc.servers[event.server].shutdown(message)
