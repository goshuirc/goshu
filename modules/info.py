#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from gbot.modules import Module, json_dumps
import os


class info(Module):
    """Provides debugging info to admins when necessary."""
    core = True

    def info(self, event, command, usercommand):
        """Output bot debug info

        @call_level owner
        """
        pretty_json = json_dumps(self.bot.irc.servers[event.server].info,
                                 sort_keys=True, indent=4)

        info_filename = os.sep.join(['config', 'modules', 'info_dict.json'])
        with open(info_filename, 'w', encoding='utf-8') as info_file:
            info_file.write(pretty_json)
            info_file.write('\n')

        self.bot.gui.put_line('info: debugging info written to: {}'.format(info_filename))
