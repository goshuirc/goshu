#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import os

from gbot.modules import Module
from gbot.libs.helper import filename_escape


class suggest(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'suggest': [self.suggest, '[-section] <suggestion> --- suggest something, anything at all'],
            },
        }

    def suggest(self, event, command, usercommand):
        if usercommand.arguments == '':
            return
        if usercommand.arguments[0] == '-':
            if len(usercommand.arguments[1:].split()) < 2:
                return
            section = filename_escape(usercommand.arguments[1:].split()[0])  # first word excluding leading -
            suggestion = usercommand.arguments[1:].split(' ', 1)[1]
        else:
            section = 'global'
            suggestion = usercommand.arguments

        output = [
            event.server + ' ' + event.source,
            '        ' + suggestion
        ]

        if not os.path.exists('suggestions'):
            os.makedirs('suggestions')

        path = 'suggestions'+os.sep+section
        outfile = open(path, 'a', encoding='utf-8')
        for line in output:
            outfile.write(line + '\n')
        outfile.close()
