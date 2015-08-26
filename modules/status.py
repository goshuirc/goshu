#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from gbot.modules import Module


class status(Module):
    core = True

    def cmd_status(self, event, command, usercommand):
        """See how the bot is going

        @view_level admin
        """
        server_count = 0
        server_info = ''

        for server in self.bot.irc.servers:
            server_count += 1
            server_info += self.bot.irc.servers[server].info['name'] + ': '
            server_info += 'Connected to ' + str(len(self.bot.irc.servers[server].info['channels'])) + ' channels'
            server_info += ', '
            server_info += str(len(self.bot.irc.servers[server].info['users'])) + ' users online ;  '

        response = '*** Status:  ' + server_info[:-5]

        event['source'].msg(response)
