#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

# Quite a lot of this module was taken, with permission, from
#   https://github.com/electronicsrules/megahal
# In particular, the regexes and the display layout. Thanks a bunch, bro!

import re
import time

from girc.formatting import escape, unescape
from girc.utils import CaseInsensitiveDict

from gbot.libs.helper import get_url, format_extract, JsonHandler
from gbot.modules import Module


class Cooldown:
    def __init__(self, cooldown_seconds=15, multiple=2, max_cooldown=60*60*24):
        self.cooldown_seconds = cooldown_seconds
        self.end_ts = time.time()
        self.default_multiple = multiple
        self.multiple = multiple
        self.max_cooldown = max_cooldown

    def can_do(self):
        if time.time() > self.end_ts:
            self.multiple = self.default_multiple
            self.end_ts = time.time() + self.cooldown_seconds
            return True

        self.multiple *= self.default_multiple
        cooldown = min(self.cooldown_seconds * self.multiple, self.max_cooldown)
        self.end_ts = time.time() + cooldown
        return False


class link(Module):
    standard_admin_commands = ['ignore']

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.links = []
        self.cooldowns = {}
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
        if event['source'].is_me or self.is_ignored(event['from_to']):
            return

        url_matches = re.search('(?:https?://)(\\S+)', unescape(event['message']))
        if not url_matches:
            return

        for url in url_matches.groups():
            response = ''
            for provider in self.links:
                if provider not in self.cooldowns:
                    self.cooldowns[provider] = CaseInsensitiveDict()
                matches = re.match(self.links[provider]['match'], url)
                if matches:
                    # response = '*** {}: '.format(self.links[provider]['display_name'])
                    response = ''

                    complete_dict = {}
                    complete_dict.update(self.get_required_values(provider))
                    for key, value in matches.groupdict().items():
                        complete_dict[key] = escape(value)

                    # check cooldown
                    server_name = event['server'].name
                    if event['from_to'].is_user:
                        from_to = event['from_to'].host
                    else:
                        from_to = event['from_to'].name

                    if server_name not in self.cooldowns[provider]:
                        self.cooldowns[provider][server_name] = event['server'].idict()
                    if from_to not in self.cooldowns[provider][server_name]:
                        self.cooldowns[provider][server_name][from_to] = Cooldown()
                    if not self.cooldowns[provider][server_name][from_to].can_do():
                        continue

                    # getting the actual file itself
                    api_url = self.links[provider]['url'].format(**complete_dict)
                    r = get_url(api_url)

                    display_name = self.links[provider]['display_name']

                    if isinstance(r, str):
                        event['from_to'].msg('*** {}: {}'.format(display_name, r))
                        return

                    # parsing
                    response += format_extract(self.links[provider], r.text,
                                               debug=True,
                                               fail='*** {}: Failed'.format(display_name))

            # remove urls from our response
            url_matches = re.search('(?:https?://)(\\S+)', response)
            if url_matches:
                for url in url_matches.groups():
                    for provider in self.links:
                        matches = re.match(self.links[provider]['match'], url)
                        if matches:
                            response = response.replace(url, '[REDACTED]')

            if response:
                event['from_to'].msg(response)
            return  # don't spam us tryna return every title
