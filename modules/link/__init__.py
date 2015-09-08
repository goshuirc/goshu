#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

# Quite a lot of this module was taken, with permission, from
#   https://github.com/electronicsrules/megahal
# In particular, the regexes and the display layout. Thanks a bunch, bro!

import re

from girc.formatting import unescape

from gbot.libs.helper import get_url, format_extract, JsonHandler
from gbot.modules import Module


class link(Module):
    standard_admin_commands = ['ignore']

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.links = []
        self.json_handlers.append(JsonHandler(self, self.dynamic_path,
                                              attr='links', ext='lnk', yaml=True,
                                              callback_name='_link_json_callback'))

    def _link_json_callback(self, new_json):
        for key, info in new_json.items():
            for var_name, var_info in info.get('required_values', {}).items():
                base_name = info['name'][0]
                self._parse_required_value(base_name, var_name, var_info)

    def link_listener(self, event):
        """Listens for links for which we can provide info

        @listen pubmsg
        @listen privmsg
        """
        if self.is_ignored(event['from_to']):
            return

        url_matches = re.search('(?:https?://)(\\S+)', unescape(event['message']))
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
                    complete_dict.update(self.get_required_values(provider))
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

                    display_name = self.links[provider]['display_name']

                    if isinstance(r, str):
                        event['from_to'].msg('*** {}: {}'.format(display_name, r))
                        return

                    # parsing
                    response += format_extract(self.links[provider], r.text,
                                               debug=True,
                                               fail='*** {}: Failed'.format(display_name))

            if response:
                event['from_to'].msg(response)
            return  # don't spam us tryna return every title
