#!/usr/bin/env python3
# Goshu IRC Bot
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

        values = {}
        for var_name, var_info in command.json.get('required_values', {}).items():
            key = ['apis', command.base_name, var_name]
            var_value = self.store.get(key)
            values[var_name] = var_value

        url = command.json['url'].format(escaped_query=urllib.parse.quote_plus(unescape(usercommand.arguments)), **values)
        r = get_url(url)

        if isinstance(r, str):
            self.bot.irc.msg(event, unescape('*** {}: {}'.format(command.json['display_name'], r)), 'public')
            return

        # parsing
        tex = r.text
        response = format_extract(command.json, tex, fail='No results')
        self.bot.irc.msg(event, response, 'public')

    def _json_command_callback(self, *args, **kwargs):
        Module._json_command_callback(self, *args, **kwargs)

        # make sure we have key to store api values
        if not self.store.has_key('apis'):
            self.store.set('apis', {})

        # handle any values that need to be stored
        for name, info in self.dynamic_commands.items():
            for var_name, var_info in info.get('required_values', {}).items():
                var_key = ['apis', name, var_name]

                var_type = var_info.get('type', 'str')
                if 'type' in var_info:
                    del var_info['type']

                if var_type == 'str':
                    var_type = str
                elif var_type == 'int':
                    var_type = int
                elif var_type == 'float':
                    var_type = float
                elif var_type == 'bool':
                    var_type = bool
                else:
                    raise Exception('key type not in list:', var_type)

                prompt = var_info.get('prompt', name)
                if 'prompt' in var_info:
                    del var_info['prompt']
                if isinstance(prompt, str):
                    prompt = prompt.rstrip() + ' '

                self.store.add_key(var_type, var_key, prompt, **var_info)
