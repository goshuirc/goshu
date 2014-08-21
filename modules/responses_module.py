#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.girclib import unescape
from gbot.libs.helper import filename_escape, utf8_bom
import random
import os
import sys
import json


class responses_module(Module):

    def __init__(self):
        Module.__init__(self)
        random.seed()

        # /s means source, the nick of whoever did the command
        # /t means target, either whoever they write afterwards, or the current self nick
        # note: /S and /T represent allcaps versions of /s and /t
        # /m at the start means: send this line as a /me rather than a /msg

    def combined(self, event, command, usercommand):
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
                'prefix': self.bot.settings.store['prefix'],
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
