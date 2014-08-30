#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.helper import split_num


class commands(Module):
    """Provides general IRC commands such as msg, me, join, part."""

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'msg': [self.msg, '<target> <message> --- send a /msg', 5],
                'me': [self.me, '<target> <message> --- send a /me', 5],
                'join': [self.join, '<channel> --- join channel', 5],
                'part': [self.part, '<channel> [reason] --- leave channel', 5],
            },
        }

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
