#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
import os
import json


class info(Module):
    """Provides debugging info to admins when necessary."""

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'info': [self.info, 'output bot debug info', 10],
            },
        }

    def info(self, event, command, usercommand):
        pretty_json = json.dumps(self.bot.irc.servers[event.server].info, sort_keys=True, indent=4)

        info_filename = os.sep.join(['config', 'modules', 'info.json'])
        info_file = open(info_filename, 'w', encoding='utf-8')
        self.bot.gui.put_line('info: debugging info written to: {}'.format(info_filename))
        info_file.write(pretty_json)
