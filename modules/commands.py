#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.helper import split_num
from gbot.users import USER_LEVEL_ADMIN, USER_LEVEL_SUPERADMIN


class commands(Module):
    """Provides general IRC commands such as msg, me, join, part."""

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'msg': [self.msg, '<target> <message> --- send a /msg', USER_LEVEL_ADMIN],
                'me': [self.me, '<target> <message> --- send a /me', USER_LEVEL_ADMIN],
                'join': [self.join, '<channel> --- join channel', USER_LEVEL_ADMIN],
                'part': [self.part, '<channel> [reason] --- leave channel', USER_LEVEL_ADMIN],

                'shutdown': [self.shutdown, '[message] -- shutdown goshu', USER_LEVEL_SUPERADMIN]
            },
        }

    # irc
    def msg(self, event, command, usercommand):
        msg_target, msg_msg = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].privmsg(msg_target, msg_msg)

    def me(self, event, command, usercommand):
        msg_target, msg_msg = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].action(msg_target, msg_msg)

    def join(self, event, command, usercommand):
        channel, key = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].join(channel, key)

    def part(self, event, command, usercommand):
        channel, reason = split_num(usercommand.arguments)

        self.bot.irc.servers[event.server].part(channel, reason)

    # goshu control
    def shutdown(self, event, command, usercommand):
        message = usercommand.arguments
        self.bot.irc.servers[event.server].shutdown(message)
