#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module


class invite(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'addchan': [self.list, "--- add the currently joined channel to our autojoin list"],
            },
            'in': {
                'invite': [(0, self.invite)],
            },
        }

    def invite(self, event):
        self.bot.irc.servers[event.server].join(event.arguments[0])
        self.bot.irc.servers[event.server].privmsg(event.arguments[0], 'Thanks for inviting me, {nick}. To keep me in here, type: {pre}addchan'.format(nick=event.source.split('!')[0]), pre=self.bot.settings.store['prefix'])
