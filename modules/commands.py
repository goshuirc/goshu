#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from gbot.modules import Module
from gbot.libs.helper import split_num


class commands(Module):
    """Provides general IRC commands such as msg, me, join, part."""
    core = True

    # irc
    def acmd_me(self, event, command, usercommand):
        """Send a /me

        @global
        @usage <target> <message>
        """
        msg_target, msg_msg = split_num(usercommand.arguments)

        event['server'].action(msg_target, msg_msg)

    def acmd_msg(self, event, command, usercommand):
        """Send a /msg

        @global
        @usage <target> <message>
        """
        msg_target, msg_msg = split_num(usercommand.arguments)

        event['server'].msg(msg_target, msg_msg)

    def acmd_notice(self, event, command, usercommand):
        """Send a /notice

        @global
        @usage <target> <message>
        """
        msg_target, msg_msg = split_num(usercommand.arguments)

        event['server'].notice(msg_target, msg_msg)

    def acmd_join(self, event, command, usercommand):
        """Join a channel

        @global
        @usage <channel>
        """
        channel, key = split_num(usercommand.arguments)

        event['server'].join_channel(channel, key)

    def acmd_part(self, event, command, usercommand):
        """Leave a channel

        @global
        @usage <channel>
        """
        channel, reason = split_num(usercommand.arguments)

        event['server'].part_channel(channel, reason)

    # goshu control
    def acmd_shutdown(self, event, command, usercommand):
        """Shutdown bot

        @global
        @usage [quit message]
        @call_level superadmin
        """
        message = usercommand.arguments
        event['server'].shutdown(message)
