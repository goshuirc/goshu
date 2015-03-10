#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module


class status(Module):
    core = True

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'status': [self.status, "--- see how imouto's going"],
            },
        }

    def status(self, event, command, usercommand):
        server_count = 0
        server_info = ''

        for server in self.bot.irc.servers:
            server_count += 1
            server_info += self.bot.irc.servers[server].info['name'] + ': '
            server_info += 'Connected to ' + str(len(self.bot.irc.servers[server].info['channels'])) + ' channels'
            server_info += ', '
            server_info += 'I can see ' + str(len(self.bot.irc.servers[server].info['users'])) + ' users  ;  '

        response = '*** Status:  ' + server_info[:-5]

        self.bot.irc.msg(event, response, 'public')
