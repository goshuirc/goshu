#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import urllib.parse

from gbot.modules import Module
from gbot.libs.girclib import unescape
from gbot.libs.helper import get_url, format_extract


class apiquery(Module):

    def combined(self, event, command, usercommand):
        if usercommand.arguments == '':
            usercommand.arguments = ' '

        url = command.json['url'].format(escaped_query=urllib.parse.quote_plus(unescape(usercommand.arguments)))
        r = get_url(url)

        if isinstance(r, str):
            self.bot.irc.msg(event, unescape('*** {}: {}'.format(command.json['display_name'], r)), 'public')
            return

        # parsing
        tex = r.text
        response = format_extract(command.json, tex, fail='No results')
        self.bot.irc.msg(event, response, 'public')
