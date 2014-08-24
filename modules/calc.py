#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.girclib import escape
from gbot.libs.fourfn import NumericStringParser, NumericStringParsingException


class calc(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                ('calc', 'c'): [self.calculate_result, '<query> --- calculate the given input'],
            },
        }

        self.parser = NumericStringParser()

    def calculate_result(self, event, command, usercommand):
        try:
            response = '*** Calc: {}'.format(escape(str(self.parser.eval(usercommand.arguments))))
        except NumericStringParsingException:
            response = '*** Could not evaluate expression.'

        self.bot.irc.msg(event, response, 'public')
