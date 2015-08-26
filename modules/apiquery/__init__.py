#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import urllib.parse

from girc.formatting import unescape

from gbot.modules import Module
from gbot.libs.helper import get_url, format_extract


class apiquery(Module):

    def combined(self, event, command, usercommand):
        if usercommand.arguments == '':
            usercommand.arguments = ' '

        values = self.get_required_values(command.base_name)
        values.update({
            'escaped_query': urllib.parse.quote_plus(unescape(usercommand.arguments))
        })

        url = command.json['url'].format(**values)
        r = get_url(url)

        if isinstance(r, str):
            event['from_to'].msg(unescape('*** {}: {}'.format(command.json['display_name'], r)))
            return

        # parsing
        tex = r.text
        response = format_extract(command.json, tex, fail='No results')
        event['from_to'].msg(response)
