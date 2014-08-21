#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from time import strftime, localtime, gmtime
import random
import os

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
from gbot.libs.helper import filename_escape


class a_log_display(Module):  # a_ at the beginning so goshu calls this module first… apparently priority's broken, too

    def __init__(self):
        Module.__init__(self)
        self.events = {
            '*' : {
                '*' : [(-20, self.handler, True)],  # sync
            }
        }
        self.nick_colors = {}
        self.logfiles_open = {}
        random.seed()

    def handler(self, event):
        if event.type == 'all_raw_messages':
            return

        #> 15:26:43
        output = '@c14'
        output += strftime("%H:%M:%S", localtime())

        #> -rizon-
        output += ' @c2-@c'
        output += event.server
        output += '@c2-@c '

        targets = ['all']

        if event.type == '':
            ...

        elif event.type in ['welcome', 'yourhost', 'created', 'myinfo',
                            'featurelist', 'luserclient', 'luserop',
                            'luserchannels', 'luserme', 'n_local',
                            'n_global', 'luserconns', 'luserunknown',
                            'motdstart', 'motd', 'endofmotd', '042', ]:
            #for message in event.arguments:
            #    output += message + ' '
            output += ' '.join(event.arguments)

        elif event.type in ['privnotice', '439', ]:
            targets.append(event.source.split('!')[0])
            output += '@c14-'
            output += '@c13' + event.source.split('!')[0]
            try:
                output += '@c14('
                output += '@c13' + escape(event.source.split('!')[1])
                output += '@c14)'
            except IndexError:
                output = output[:-1]
            output += '-@c '
            output += event.arguments[0]

        elif event.type in ['pubmsg', ]:
            targets.append(event.target)
            output += '@c3-@c'
            output += escape(event.target)
            output += '@c3- '
            output += '@c14<@c'
            try:
                selected_mode = ''

                for mode in ['~', '&', '@', '%', '+']:
                    if mode in self.bot.irc.servers[event.server].info['channels'][event.target]['users'][event.source.split('!')[0]]:
                        output += escape(mode)
                        selected_mode = mode
                        break

                if not selected_mode:
                    output += ' '
            except:
                output += ' '
            output += self.nick_color(event.source.split('!')[0])
            output += '@c14>@c '
            output += event.arguments[0]

        elif event.type in ['privmsg', ]:
            output += '@c3-@c'
            if event.direction == 'in':
                output += escape(event.source.split('!')[0])
                targets.append(event.source.split('!')[0])
            else:
                output += event.target
                targets.append(event.target)
            output += '@c3- '
            output += '@c14<@c'
            output += self.nick_color(event.source.split('!')[0])
            output += '@c14>@c '
            output += event.arguments[0]

        elif event.type in ['action', ]:
            output += '@c3-@c'
            if event.direction == 'in':
                output += event.from_to
                targets.append(event.from_to)
            else:
                output += event.target
                targets.append(event.target)
            output += '@c3-@c  @b* '
            output += event.source.split('!')[0] + '@b '
            output += event.arguments[0]

        elif event.type in ['umode', ]:
            output += 'Mode change '
            output += '@c14[@c'
            output += event.arguments[0]
            output += '@c14]@c'
            output += ' for user '
            output += event.target

        elif event.type in ['mode', ]:
            targets.append(event.target)
            output += '@c6-@c!@c6-@c '
            output += 'mode/'
            output += '@c10' + event.target + '@c '
            output += '@c14[@c'
            for arg in event.arguments:
                output += arg + ' '
            output = output[:-1]  # strip last space
            output += '@c14]@c'
            output += ' by @b'
            output += event.source.split('!')[0]

        elif event.type in ['kick', ]:
            targets.append(escape(event.target))
            output += '@c6-@c!@c6-@c10 '
            output += event.arguments[0]
            output += '@c was kicked from '
            output += escape(event.target)
            output += ' by '
            output += event.source.split('!')[0]
            output += ' @c14[@c'
            output += event.arguments[1]
            output += '@c14]@c'

        elif event.type in ['join', ] and event.direction == 'in':
            targets.append(event.target)
            output += '@c6-@c!@c6-@b@c10 '
            output += event.source.split('!')[0]
            output += '@b @c14[@c10'
            output += event.source.split('!')[1]
            output += '@c14]@c '
            output += 'has joined @b'
            output += escape(event.target)

        elif event.type in ['nick', ]:
            output += '@c6-@c!@c6-@c10 '
            output += event.source.split('!')[0]
            output += '@c is now known as @c10'
            output += str(event.target)

        elif event.type in ['currenttopic', ]:
            targets.append(event.arguments[0])
            output += '@c6-@c!@c6-@c10 Topic for @c10'
            output += event.arguments[0]
            output += '@c: '
            output += event.arguments[1]

        elif event.type in ['quit', ]:
            output += '@c6-@c!@c6-@c10 '
            output += event.source.split('!')[0]
            output += ' @c14[@c'
            output += event.source.split('!')[1]
            output += '@c14]@c has quit @c14[@c'
            output += event.arguments[0]
            output += '@c14]@c'

        elif event.type in ['ctcp', ] and event.arguments[0] == 'ACTION':
            return

        elif event.type in ['ping', 'pong', ]:
            return

        else:
            targets.append('tofix')
            output += str(event.direction) + ' ' + str(event.type) + ' ' + str(event.source) + ' ' + str(event.target) + ' ' + escape(str(event.arguments))

        self.bot.gui.put_line(output)
        self.log(output, event.server, targets)

    def log(self, output, server='global', targets=['global']):
        server_escape = filename_escape(server)
        targets_escape = []
        for target in targets:
            targets_escape.append(filename_escape(target))
        for target in targets_escape:
            if not os.path.exists('logs'):
                os.makedirs('logs')
            if not os.path.exists('logs/'+server):
                os.makedirs('logs/'+server)
            path = 'logs/'+server_escape+'/'+target+'.log'

            if target not in self.logfiles_open or not os.path.exists(path):
                output = '@c14 Logfile Opened - ' + strftime("%A %B %d, %H:%M:%S %Y", localtime()) + '\n' + output
                self.logfiles_open[target] = strftime("%A %B %d", localtime())
            elif self.logfiles_open[target] != strftime("%A %B %d", localtime()):
                output = '@c14 New Day - ' + strftime("%A %B %d, %H:%M:%S %Y", localtime()) + '\n' + output
                self.logfiles_open[target] = strftime("%A %B %d", localtime())

            outfile = open(path.lower(), 'a', encoding='utf-8')
            outfile.write(unescape(output) + '\n')
            outfile.close()

    def nick_color(self, nickhost):
        nick = nickhost.split('!')[0]
        if nick not in self.nick_colors:
            self.nick_colors[nick] = random.randint(2, 13)
        return '@c' + str(self.nick_colors[nick]) + nick
