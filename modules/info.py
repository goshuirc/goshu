#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
import os
import json


class info(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'info': [self.info, 'output bot debug info', 10],
            },
        }

    def info(self, event, command, usercommand):
        pretty_json = json.dumps(self.bot.irc.servers[event.server].info, sort_keys=True, indent=4)

        info_file = open('config'+os.sep+'modules'+os.sep+'info.json', 'w', encoding='utf-8')
        info_file.write(pretty_json)
