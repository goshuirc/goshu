#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import os

from gbot.modules import Module
from gbot.libs.helper import filename_escape


class suggest(Module):
    core = True

    def cmd_suggest(self, event, command, usercommand):
        """Suggest something, anything at all!

        @usage [-section] <suggestion>
        """
        if usercommand.arguments == '':
            return
        if usercommand.arguments[0] == '-':
            if len(usercommand.arguments[1:].split()) < 2:
                return
            # first word excluding leading -
            section = filename_escape(usercommand.arguments[1:].split()[0])
            suggestion = usercommand.arguments[1:].split(' ', 1)[1]
        else:
            section = 'global'
            suggestion = usercommand.arguments

        output = [
            event['server'].name + ' ' + event['source'].nickmask,
            '        ' + suggestion
        ]

        if not os.path.exists('suggestions'):
            os.makedirs('suggestions')

        path = os.path.join('suggestions', section)
        outfile = open(path, 'a', encoding='utf-8')
        for line in output:
            outfile.write(line + '\n')
        outfile.close()
