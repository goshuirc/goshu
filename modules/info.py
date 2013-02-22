#!/usr/bin/env python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
import os
import json


class info(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands' : {
                'info' : [self.info, 'output bot debug info', 10],
            },
        }

    def info(self, event, command, usercommand):
        pretty_json = json.dumps(self.bot.irc.servers[event.server].info, sort_keys=True, indent=4)

        info_file = open('config'+os.sep+'modules'+os.sep+'info.json', 'w', encoding='utf-8')
        info_file.write(pretty_json)
