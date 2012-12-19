#!/usr/bin/env python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module

class invite(Module):
    name = "invite"

    def __init__(self):
        self.events = {
            'in' : {
                'invite' : [(0, self.invite)],
            },
        }

    def invite(self, event):
        self.bot.irc.servers[event.server].join(event.arguments[0])
        self.bot.irc.servers[event.server].privmsg(event.arguments[0], 'Thanks for inviting me, ' + event.source.split('!')[0])
