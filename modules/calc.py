#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.libs.helper import filename_escape
import wolframalpha
import json
import os

from gbot.modules import Module
from gbot.libs.girclib import escape
from gbot.libs.nsp import NumericStringParser


class calc(Module):
    """Lets users calculate math, convert figures, and all sorts of fun stuff thanks to W|A!"""

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                ('calc', 'c'): [self.calculate_result, '<query> --- calculate the given input'],
            },
        }

        self.parser = NumericStringParser()
        self.wolfram = None

        wolfram_filename = os.sep.join(['config', 'modules', '{}.json'.format(filename_escape(self.name))])
        try:
            wolfram_info = json.loads(open(wolfram_filename).read())

            self.wolfram_api_key = wolfram_info['key']
            self.wolfram = wolframalpha.Client(self.wolfram_api_key)
        except:
            self.bot.gui.put_line('wolfram: Wolfram Alpha app key file error: {}'.format(wolfram_filename))
            return

    def calculate_result(self, event, command, usercommand):
        try:
            response = '*** Calc: {}'.format(escape(str(self.parser.eval(usercommand.arguments))))
        except:
            fail = '*** Could not evaluate expression.'

            if self.wolfram:
                try:
                    res = self.wolfram.query(usercommand.arguments)
                    if len(res.pods) > 1:
                        answer = res.pods[1].text
                        answer = answer.encode('unicode-escape').replace(b'\\\\:', b'\u').decode('unicode-escape')  # to fix unicode
                        response = '*** W|A: {}'.format(escape(answer))
                    else:
                        response = fail
                except Exception as ex:
                    if 'Computation error' in str(ex):
                        response = fail
                    else:
                        print('exception:', ex)
                        response = '*** Sorry, we ran into a problem. Please try again later'
            else:
                response = fail

        self.bot.irc.msg(event, response, 'public')
