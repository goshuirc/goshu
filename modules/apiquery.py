#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import urllib.parse

from gbot.modules import Module
from gbot.libs.girclib import unescape
from gbot.libs.helper import get_url, format_extract


class apiquery(Module):

    def combined(self, event, command, usercommand):
        if usercommand.arguments == '':
            usercommand.arguments = ' '

        url = command.json['url'].format(escaped_query=urllib.parse.quote_plus(unescape(usercommand.arguments))[2:])
        r = get_url(url)

        if isinstance(r, str):
            self.bot.irc.msg(event, unescape('*** {}: {}'.format(command.json['display_name'], r)), 'public')
            return

        # parsing
        response = format_extract(command.json, r.text, fail='No results')
        self.bot.irc.msg(event, response, 'public')
