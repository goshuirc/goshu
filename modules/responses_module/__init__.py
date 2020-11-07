#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel$danieloaks.net>
# licensed under the ISC license

import json
import os
import random

from girc.formatting import unescape

from gbot.modules import Module


class responses_module(Module):
    """Supports creating special custom commands with simple json dictionaries."""
    standard_admin_commands = ['ignore']

    def __init__(self, bot):
        Module.__init__(self, bot)

        random.seed()

        # $s means source, the nick of whoever did the command
        # $t means target, either whoever they write afterwards, or the current self nick
        # note: $S and $T represent allcaps versions of $s and $t
        # $f at the start means: ignore the standard pre / post lines
        # $m at the start means: send this line as a /me rather than a /msg

    def acmd_create(self, event, command, usercommand):
        """Create new responses skeletons dynamically

        @usage <name>
        """
        cmd_name, args = usercommand.arg_split(1)

        if not cmd_name:
            event['source'].msg('You must give me a name for the response you want to create')
            return

        filename = os.path.join(self.dynamic_path, cmd_name.lower())
        filename += '.res.json'

        if os.path.exists(filename):
            event['source'].msg('That module already exists, ignoring')
            return

        new_response_dict = {
            'description': '-- Description Here',
            'call_level': 10,
            'view_level': 10,
            'channel_whitelist': '#example',
            '1': [
                '$s sent me a message!'
            ],
            '1pre': '',
            '1post': '',
            '2': [
                '$s wants me to talk to $t!'
            ],
            '2pre': '',
            '2post': '',
        }

        with open(filename, 'w', encoding='utf-8') as module_file:
            module_file.write('{}\n'.format(json.dumps(new_response_dict,
                                                       sort_keys=True, indent=4)))

        event['source'].msg('New responses file created in {}'.format(filename))
        event['source'].msg('By default this responses file will not be accessible by '
                            'ordinary users, and will be channel-restricted, so you must '
                            'modify it on-disk to do what you want!')

    def combined(self, event, command, usercommand):
        if self.is_ignored(event['from_to']):
            return

        source = event['source'].nick
        if usercommand.arguments.strip() == '':
            target = event['server'].nick
            num = '1'
        else:
            target = usercommand.arguments.strip()
            num = '2'

        # message = initial, 1/2pre, line(s), 1/2post, outro

        output = []

        if 'initial' in command.json:
            if type(command.json['initial']) == list:
                for line in command.json['initial']:
                    output.append(line)
            else:
                output.append(command.json['initial'])

        pre = ''
        if num + 'pre' in command.json:
            pre = command.json[num + 'pre']

        post = ''
        if num + 'post' in command.json:
            post = command.json[num + 'post']

        if num == '2':
            if num not in command.json:
                num = '1'

        response_list = command.json[num]
        response_num = random.randint(1, len(response_list)) - 1
        random.shuffle(response_list)
        response = response_list[response_num]

        if response[0:2] == '$f':
            pre = ''
            post = ''
            response = response[2:]

        if type(response) == str:
            response = [response]
        for line in response:
            output.append(pre + line + post)

        for line in output:
            use_action = False
            if line[:2] == '$m':
                line = line[2:]
                use_action = True

            line = unescape(line, {
                's': source,
                'S': source.upper(),
                't': target,
                'T': target.upper(),
                'prefix': self.bot.settings.store['command_prefix'],
                'randomchannelnick': [random_channel_nick, [self.bot, event]]
            })

            if use_action:
                event['from_to'].me(line.strip())
            else:
                event['from_to'].msg(line)


def random_channel_nick(bot, event):
    try:
        user_list = list(event['from_to'].users.keys())
        user_num = random.randint(1, len(user_list)) - 1
        if len(user_list) > 1:
            while user_list[user_num] == event['source'].nick:
                user_num = random.randint(1, len(user_list)) - 1
        return user_list[user_num]

    except:
        return event['source'].nick
