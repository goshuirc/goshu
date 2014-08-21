#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module


class invite(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'in' : {
                'invite' : [(0, self.invite)],
            },
        }

    def invite(self, event):
        self.bot.irc.servers[event.server].join(event.arguments[0])
        self.bot.irc.servers[event.server].privmsg(event.arguments[0], 'Thanks for inviting me, ' + event.source.split('!')[0])
