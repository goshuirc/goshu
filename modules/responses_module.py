#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import os
import json
import random

from gbot.modules import Module, cmd_split, std_ignore_command
from gbot.libs.girclib import unescape
from gbot.users import USER_LEVEL_ADMIN


class responses_module(Module):
    """Supports creating special custom commands with simple json dictionaries."""
    def __init__(self, bot):
        Module.__init__(self, bot)

        random.seed()

        # @s means source, the nick of whoever did the command
        # @t means target, either whoever they write afterwards, or the current self nick
        # note: @S and @T represent allcaps versions of @s and @t
        # @f at the start means: ignore the standard pre / post lines
        # @m at the start means: send this line as a /me rather than a /msg

    def cmd_response(self, event, command, usercommand):
        """Ignore a certain target
        @usage ignore add <target>

        @description List ignored targets
        @usage ignore list

        @description Create a blank response under the given name
        @usage create <name>

        @call_level admin
        """
        if not usercommand.arguments:
            return

        do, args = cmd_split(usercommand.arguments)

        if do == 'ignore':
            do, args = cmd_split(args)

            std_ignore_command(self, event, do, args)

        elif do == 'create':
            if len(usercommand.arguments.split()) > 1:
                module_name = args.lower().split()[0]
                filename = os.path.join('modules/responses_module', module_name)
                filename += '.res.json'

                if os.path.exists(filename):
                    self.bot.irc.msg(event, 'That module already exists, ignoring')
                    return
            else:
                self.bot.irc.msg(event, 'You must give me name for the response you want to create')
                return

            new_response_dict = {
                'description': '-- Description Here',
                'call_level': 10,
                'view_level': 10,
                'channel_whitelist': '#example',
                '1': [
                    '@s sent me a message!'
                ],
                '1pre': '',
                '1post': '',
                '2': [
                    '@s wants me to talk to @t!'
                ],
                '2pre': '',
                '2post': '',
            }

            with open(filename, 'w') as module_file:
                module_file.write('{}\n'.format(json.dumps(new_response_dict, sort_keys=True, indent=4)))

            self.bot.irc.msg(event, 'New responses file created in {}'.format(filename))
            self.bot.irc.msg(event, 'By default this responses file will not be accessible by ordinary users,'
                                    ' and will be channel-restricted, so you must modify it on-disk to do'
                                    ' what you want!')

    def combined(self, event, command, usercommand):
        if self.is_ignored(event.from_to):
            return

        source = event.source.split('!')[0]
        if usercommand.arguments.strip() == '':
            target = self.bot.irc.servers[event.server].info['connection']['nick']
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

        if response[0:2] == '@f':
            pre = ''
            post = ''
            response = response[2:]

        if type(response) == str:
            response = [response]
        for line in response:
            output.append(pre + line + post)

        for line in output:
            line = unescape(line)
            line = unescape(line, {
                's': source,
                'S': source.upper(),
                't': target,
                'T': target.upper(),
                'prefix': self.bot.settings.store['command_prefix'],
                'randomchannelnick': [random_channel_nick, [self.bot, event]]
            })

            if line[0:2] == '@m':
                self.bot.irc.action(event, line[2:].strip(), 'public')
            else:
                self.bot.irc.msg(event, line, 'public')


def random_channel_nick(arg_list):
    bot, event = arg_list

    try:
        user_list = list(bot.irc.servers[event.server].info['channels'][event.from_to]['users'].keys())
        user_num = random.randint(1, len(user_list)) - 1
        if len(user_list) > 1:
            while user_list[user_num] == event.source.split('!')[0]:
                user_num = random.randint(1, len(user_list)) - 1
        return user_list[user_num]
    except:
        return event.source.split('!')[0]
