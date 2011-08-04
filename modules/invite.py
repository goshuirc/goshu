#!/usr/bin/env python
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
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