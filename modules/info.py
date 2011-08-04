#!/usr/bin/env python
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
import json

class info(Module):
    name = "info"
    
    def __init__(self):
        self.events = {
            'commands' : {
                'info' : [self.info, 'get bot info', 10],
            },
        }
    
    def info(self, event, command):
        print(json.dumps(self.bot.irc.servers[event.server].info, sort_keys=True, indent=4))