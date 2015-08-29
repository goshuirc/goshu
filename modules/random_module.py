#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from gbot.modules import Module
import random


class random_module(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)

        random.seed()

    def cmd_random(self, event, command, usercommand):
        """Random selection from phrases separated by a |

        @usage <first>|<second>|<third>...
        """
        response = event['source'].nick + ': '

        random_list = usercommand.arguments.split('|')
        random_num = random.randint(1, len(random_list)) - 1

        response += random_list[random_num].strip()

        if random_list[random_num].strip() != '':
            event['from_to'].msg(response)
