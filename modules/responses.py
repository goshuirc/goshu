#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.helper import filename_escape, utf8_bom
import random
import os
import sys
import json


class responses(Module):
    name = 'responses'

    def __init__(self):
        self.events = {
            'commands' : {
                '*' : [self.combined, '--- handle responses', 0],
            },
        }
        self.responses_path = 'modules'+os.sep+'responses'
        random.seed()

    def commands(self):
        output = Module.commands(self)
        for (dirpath, dirs, files) in os.walk(self.responses_path):
            for file in files:
                try:
                    (name, ext) = os.path.splitext(file)
                    if ext == os.extsep + 'json':
                        f = open(dirpath+os.sep+file, encoding='utf8')
                        f_read = utf8_bom(f.read())
                        info = json.loads(f_read)
                    else:
                        continue
                except ValueError:
                    continue

                if 'description' in info:
                    command_description = info['description']
                else:
                    command_description = ''
                if 'permission' in info:
                    command_permission = info['permission']
                else:
                    command_permission = 0

                output[name] = [self.combined, command_description, command_permission]
        return output

        # /s means source, the nick of whoever did the command
        # /t means target, either whoever they write afterwards, or the current self nick
        # note: /S and /T represent allcaps versions of /s and /t
        # /m at the start means: send this line as a /me rather than a /msg

    def combined(self, event, command):
        module_path = None
        for (dirpath, dirs, files) in os.walk(self.responses_path):
            for file in files:
                if not dirpath in sys.path:
                    sys.path.insert(0, dirpath)
                (name, ext) = os.path.splitext(file)
                if ext == os.extsep + 'json':
                    if name == filename_escape(command.command):
                        module_path = dirpath
        if not module_path:
            return

        try:
            f = open(module_path+os.sep+filename_escape(command.command)+os.extsep+'json', 'r', encoding='utf8')
            f_read = utf8_bom(f.read())
            responses = json.loads(f_read)
        except ValueError:
            return

        source = event.source.split('!')[0]
        if command.arguments.strip() == '':
            target = self.bot.irc.servers[event.server].info['connection']['nick']
            num = '1'
        else:
            target = command.arguments.strip()
            num = '2'

        # message = initial, 1/2pre, line(s), 1/2post, outro

        output = []

        if 'initial' in responses:
            if type(responses['initial']) == list:
                for line in responses['initial']:
                    output.append(line)
            else:
                output.append(responses['initial'])

        pre = ''
        if num + 'pre' in responses:
            pre = responses[num + 'pre']

        post = ''
        if num + 'post' in responses:
            post = responses[num + 'post']

        if num == '2':
            if num not in responses:
                num = '1'

        response_list = responses[num]
        response_num = random.randint(1, len(response_list)) - 1
        random.shuffle(response_list)
        response = response_list[response_num]

        if type(response) == str:
            response = [response]
        for line in response:
            output.append(pre + line + post)

        for line in output:
            output = self.bot.irc.unescape(output)
            output = self.bot.irc.unescape(output, {
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
