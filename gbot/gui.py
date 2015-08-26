#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import getpass

from .libs import helper


class GuiManager:
    """Handles the goshu terminal display."""

    def __init__(self, bot):
        self.bot = bot

    # update
    def update_info(self):
        line = 'Goshubot - '
        for server in self.bot.irc.servers:
            line += self.bot.irc.servers[server].info['name'] + ': '
            line += str(len(self.bot.irc.servers[server].info['channels'])) + ' Channels, '
            line += str(len(self.bot.irc.servers[server].info['users'])) + ' Users ; '
        print(line[:-3])

    def put_line(self, line):
        """Output the given line."""
        print(line)

    # input functions
    def get_string(self, prompt, repeating_prompt=None, default=None,
                   confirm_prompt=None, blank_allowed=False,
                   password=False, validate=None):
        """Get a string."""
        if repeating_prompt is None:
            repeating_prompt = prompt

        # echo typed chars vs not doing that
        if password:
            fn = getpass.getpass
        else:
            fn = input

        # confirm value if necessary
        if confirm_prompt is not None:
            val1 = fn(prompt)
            val2 = fn(confirm_prompt)

            while (val1 != val2 or (val1.strip() == '' and not blank_allowed and default is None)
                   or (validate and not validate(val1))):
                val1 = fn(repeating_prompt)
                val2 = fn(confirm_prompt)

            if val1.strip() == '' and default is not None:
                output_value = default
            else:
                output_value = val1

        # else just get a value that is / is not blank
        else:
            output_value = fn(prompt)

            if not blank_allowed or validate:
                if default is not None:
                    output_value = default
                else:
                    while output_value.strip() == '' or (validate and not validate(output_value)):
                        output_value = fn(repeating_prompt)

        return output_value

    def get_number(self, prompt, repeating_prompt=None, default=None, force_int=False, password=False):
        """Get a number, force_int to force an integer."""
        # parse function, since we repeat it
        def parse_value(val):
            try:
                if force_int or '.' not in val:
                    return int(val)
                else:
                    return float(val)
            except (ValueError, TypeError):
                if (default is not None) and (val.strip() == ''):
                    # we take blank as 'use the default'
                    # just use user-provided default
                    return default
                else:
                    return ''  # user screwed up, we'll ask for another value

        # get initial value
        value = self.get_string(prompt, repeating_prompt, blank_allowed=True, password=password).strip()
        value = parse_value(value)

        # repeat if required
        while not isinstance(value, (int, float)):
            value = self.get_string(repeating_prompt, repeating_prompt)
            value = parse_value(value)

        return value

    def get_bool(self, prompt, repeating_prompt=None, default=None, allow_none=False, password=False):
        """Get a bool, allow_none to allow None."""
        # parse function, since we repeat it
        def parse_value(val):
            if val == '':
                if default is not None or allow_none:
                    return default
            else:
                val = helper.true_or_false(val)

                if val is None:
                    return ''
                else:
                    return val

        # get initial value
        value = self.get_string(prompt, repeating_prompt, blank_allowed=True, password=password).strip()
        value = parse_value(value)

        # repeat if needed
        while value not in (True, False, None):
            value = self.get_string(repeating_prompt, repeating_prompt, blank_allowed=True, password=password).strip()
            value = parse_value(value)

        return value
