#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
import random


class random_module(Module):  # so named to prevent random lib issues

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands' : {
                'random' : [self.random_command, '--- random selection from phrases seperated by a |'],
            },
        }
        random.seed()

    def random_command(self, event, command, usercommand):
        response = event.source.split('!')[0] + ': '

        random_list = usercommand.arguments.split('|')
        random_num = random.randint(1, len(random_list)) - 1

        response += random_list[random_num].strip()

        if random_list[random_num].strip() != '':
            self.bot.irc.msg(event, response, 'public')
