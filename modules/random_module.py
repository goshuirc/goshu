#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
import random


class random_module(Module):  # so named to prevent random lib issues

    def __init__(self, bot):
        Module.__init__(self, bot)

        random.seed()

    def cmd_random(self, event, command, usercommand):
        """Random selection from phrases separated by a |"""
        response = event.source.split('!')[0] + ': '

        random_list = usercommand.arguments.split('|')
        random_num = random.randint(1, len(random_list)) - 1

        response += random_list[random_num].strip()

        if random_list[random_num].strip() != '':
            self.bot.irc.msg(event, response, 'public')
