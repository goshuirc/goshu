#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

# Quite a lot of this module was taken, with permission, from https://github.com/electronicsrules/megahal
# In particular, the regexes and the display layout. Thanks a bunch, bro!

import re

from gbot.modules import Module
from gbot.libs.girclib import unescape
from gbot.libs.helper import get_url, format_extract, JsonHandler


class link(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'in': {
                'pubmsg': [(0, self.link)],
                'privmsg': [(0, self.link)],
            },
        }
        self.links = []
        self.json_handlers.append(JsonHandler(self, 'links', self.dynamic_path, ext='lnk', yaml=True))

    def link(self, event):
        url_matches = re.search('(?:https?://)(\\S+)', unescape(event.arguments[0]))
        if not url_matches:
            return

        for url in url_matches.groups():
            response = ''
            for provider in self.links:
                matches = re.match(self.links[provider]['match'], url)
                if matches:
                    # response = '*** {}: '.format(self.links[provider]['display_name'])
                    response = ''

                    match_index = 1
                    complete_dict = {}
                    for match in matches.groups():
                        if match is not None:
                            complete_dict['regex_{}'.format(match_index)] = match
                            match_index += 1

                    match_dict = matches.groupdict()
                    for match in match_dict:
                        if match_dict[match] is not None:
                            complete_dict['regex_{}'.format(match)] = match_dict[match]

                    # getting the actual file itself
                    url = self.links[provider]['url'].format(**complete_dict)
                    r = get_url(url)

                    if isinstance(r, str):
                        self.bot.irc.msg(event, unescape('*** {}: {}'.format(self.links[provider]['display_name'], r)), 'public')
                        return

                    # parsing
                    response += format_extract(self.links[provider], r.text, fail='*** {}: Failed'.format(self.links[provider]['display_name']))

            if response:
                self.bot.irc.msg(event, response, 'public')
            return  # don't spam us tryna return every title
