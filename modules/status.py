#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module


class status(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands' : {
                'status' : [self.status, "--- see how imouto's going", 0],
            },
        }

    def status(self, event, command, usercommand):
        server_count = 0
        server_info = ''

        for server in self.bot.irc.servers:
            server_count += 1
            server_info += self.bot.irc.servers[server].info['name'] + ' -- '
            server_info += 'connected to ' + str(len(self.bot.irc.servers[server].info['channels'])) + ' channels'
            server_info += ', '
            server_info += 'tracking ' + str(len(self.bot.irc.servers[server].info['users'])) + ' users  ;  '

        response = '*** Status:  ' + server_info[:-5]

        self.bot.irc.msg(event, response, 'public')
