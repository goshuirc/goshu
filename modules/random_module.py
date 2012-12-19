#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
import random


class random_module(Module):  # so named to prevent random lib issues
    name = 'random_module'

    def __init__(self):
        self.events = {
            'commands' : {
                'random' : [self.random_command, '--- random selection from phrases seperated by a |', 0],
            },
        }
        random.seed()

    def random_command(self, event, command):
        response = event.source.split('!')[0] + ': '

        random_list = command.arguments.split('|')
        random_num = random.randint(1, len(random_list)) - 1

        response += random_list[random_num].strip()

        if random_list[random_num].strip() != '':
            self.bot.irc.msg(event, response, 'public')
