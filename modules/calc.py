#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import json
import os

from girc.formatting import escape
import wolframalpha

from gbot.libs.helper import filename_escape
from gbot.libs.nsp import NumericStringParser
from gbot.modules import Module


class calc(Module):
    """Lets users calculate math, convert figures, and all sorts of fun stuff."""

    def __init__(self, bot):
        Module.__init__(self, bot)

        self.parser = NumericStringParser()
        self.wolfram = None

        config_json_file = '{}.json'.format(filename_escape(self.name))
        calc_filename = os.sep.join(['config', 'modules', config_json_file])
        if os.path.exists(calc_filename):
            try:
                calc_info = json.loads(open(calc_filename).read())

                self.calc_api_key = calc_info['key']
            except:
                self.bot.gui.put_line('wolfram: Wolfram Alpha app key file error: {}'
                                      ''.format(calc_filename))
                return
        else:
            prompt = 'Wolfram Alpha app key for calc command: '
            self.calc_api_key = self.bot.gui.get_string(prompt)

            with open(calc_filename, 'w') as calc_file:
                calc_file.write(json.dumps({
                    'key': self.calc_api_key,
                }))

        self.wolfram = wolframalpha.Client(self.calc_api_key)

    def cmd_calc(self, event, command, usercommand):
        """Calculate the given input

        @alias c
        @usage <query>
        """
        try:
            result = str(self.parser.eval(usercommand.arguments))
            response = '*** Calc: {}'.format(escape(result))
        except:
            fail = '*** Could not evaluate expression.'

            if self.wolfram:
                try:
                    res = self.wolfram.query(usercommand.arguments)
                    if len(res.pods) > 1:
                        answer = res.pods[1].text

                        # fix unicode
                        answer = answer.encode('unicode-escape')
                        answer = answer.replace(b'\\\\:', b'\u')
                        answer = answer.decode('unicode-escape')

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

        event['from_to'].msg(response)
