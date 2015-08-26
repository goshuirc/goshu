#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel$danieloaks.net>
# licensed under the ISC license

from time import strftime, localtime
import random
import os
import datetime

from girc.formatting import escape, unescape
import colorama
colorama.init()

from gbot.modules import Module
from gbot.libs.helper import filename_escape


class log_display(Module):
    """Prints and shows IRC activity, with nice colours!"""
    core = True

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.nick_colors = {}
        self.logfiles_open = {}
        random.seed()

    def log_display_listener(self, event):
        """Writes messages to screen and log

        $listen * * high inline
        """
        if event.type == 'all_raw_messages':
            return

        # > 15:26:43
        output = '$c14'
        output += strftime("%H:%M:%S", localtime())

        # > -rizon-
        output += ' $c12-$c'
        output += event.server
        output += '$c12-$c '

        targets = ['all']

        if event.type == '':
            ...

        elif event.type in ['welcome', 'yourhost', 'created', 'myinfo',
                            'featurelist', 'luserclient', 'luserop',
                            'luserchannels', 'luserme', 'n_local',
                            'n_global', 'luserconns', 'luserunknown',
                            'motdstart', 'endofmotd', '042', 'nomotd']:
            output += escape(' '.join(event.arguments))

        elif event.type in ['motd', ]:
            output += ' '.join(event.arguments)

        elif event.type in ['privnotice', '439', ]:
            targets.append(event.source.split('!')[0])
            output += '$c14-'
            output += '$c13' + event.source.split('!')[0]
            try:
                output += '$c14('
                output += '$c13' + escape(event.source.split('!')[1])
                output += '$c14)'
            except IndexError:
                output = output[:-1]
            output += '-$c '
            output += event.arguments[0]

        elif event.type in ['cannotsendtochan', '408', ]:
            chan = escape(event.arguments[0])
            msg = escape(event.arguments[1])
            targets.append(chan)

            output += '$c3-$c'
            output += escape(chan)
            output += '$c3- '
            output += '$r$b** $c4Message Rejected$r: '
            output += msg

        elif event.type in ['pubmsg', ]:
            targets.append(event.target)
            output += '$c3-$c'
            output += escape(event.target)
            output += '$c3- '
            output += '$c14<$c'
            try:
                selected_mode = ''
                server = self.bot.irc.servers[event.server]
                channel = server.istring(event.target)
                user_nick = server.istring(event.source.split('!')[0])

                for mode in server.info['server']['isupport']['PREFIX'][1]:
                    if mode in server.get_channel_info(channel)['users'][user_nick]:
                        output += escape(mode)
                        selected_mode = mode
                        break

                if not selected_mode:
                    output += ' '
            except:
                output += ' '
            output += self.nick_color(event.source.split('!')[0])
            output += '$c14>$c '
            output += hide_pw_if_necessary(event.arguments[0], self.bot.settings.store['command_prefix'])

        elif event.type in ['privmsg', ]:
            output += '$c3-$c'
            if event.direction == 'in':
                output += escape(event.source.split('!')[0])
                targets.append(event.source.split('!')[0])
            else:
                output += event.target
                targets.append(event.target)
            output += '$c3- '
            output += '$c14<$c'
            output += self.nick_color(event.source.split('!')[0])
            output += '$c14>$c '
            output += hide_pw_if_necessary(event.arguments[0], self.bot.settings.store['command_prefix'])

        elif event.type in ['action', ]:
            output += '$c3-$c'
            if event.direction == 'in':
                output += event.from_to
                targets.append(event.from_to)
            else:
                output += event.target
                targets.append(event.target)
            output += '$c3-$c  $b* '
            output += event.source.split('!')[0] + '$b '
            if len(event.arguments):
                output += event.arguments[0]

        elif event.type in ['umode', ]:
            output += 'Mode change '
            output += '$c14[$c'
            output += event.arguments[0]
            output += '$c14]$c'
            output += ' for user '
            output += event.target

        elif event.type in ['mode', ]:
            targets.append(event.target)
            output += '$c6-$c!$c6-$c '
            output += 'mode/'
            output += '$c10' + event.target + ' '
            output += '$c14[$c'
            for arg in event.arguments:
                output += arg + ' '
            output = output[:-1]  # strip last space
            output += '$c14]$c'
            output += ' by $b'
            output += event.source.split('!')[0]

        elif event.type in ['channelmodeis', ]:
            chan = escape(event.arguments[0])
            modes = escape(' '.join(event.arguments[1:]))

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'modes:'
            output += '$c10' + chan + ' '
            output += '$c14[$c'
            output += modes
            output += '$c14]$c'

        elif event.type in ['channelcreate', ]:
            chan = escape(event.arguments[0])
            timestamp = escape(event.arguments[1])

            try:
                created_ts = datetime.datetime.fromtimestamp(int(timestamp))
            except:
                return  # malformed

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'times:'
            output += '$c10' + chan + '$c '
            output += 'Channel created $b'
            output += created_ts.strftime('%a, %d %b %Y %H:%M:%S')

        elif event.type in ['namreply', ]:
            chan = escape(event.arguments[1])
            nicks = escape(event.arguments[2])

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'nicks:'
            output += '$c10' + chan + ' '
            output += '$c14[$c'
            output += nicks
            output += '$c14]$c'

        elif event.type in ['endofnames', ]:
            chan = escape(event.arguments[0])
            user_dict = self.bot.irc.servers[event.server].get_channel_info(chan)['users']

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'stats:'
            output += '$c10' + chan + '$c: '
            output += '{} nick{} '.format(len(user_dict), 's' if len(user_dict) > 1 else '')
            output += '$c3($c'

            normal_users = 0
            voiced_users = 0
            halfop_users = 0
            op_users = 0

            for user in user_dict:
                # todo: populate and work from ISUPPORT lists
                if '$' in user_dict[user] or '!' in user_dict[user] or '&' in user_dict[user] or '~' in user_dict[user]:
                    op_users += 1
                elif '%' in user_dict[user]:
                    halfop_users += 1
                elif '+' in user_dict[user]:
                    voiced_users += 1
                else:
                    normal_users += 1

            priv_lists = []

            if op_users:
                priv_lists.append('$b{}$r ops'.format(op_users))
            if halfop_users:
                priv_lists.append('$b{}$r halfops'.format(halfop_users))
            if voiced_users:
                priv_lists.append('$b{}$r voices'.format(voiced_users))
            if normal_users:
                priv_lists.append('$b{}$r normals'.format(normal_users))

            output += ', '.join(priv_lists)

            output += '$c3)$c'

        elif event.type in ['kick', ]:
            targets.append(escape(event.target))
            output += '$c6-$c!$c6-$c10 '
            output += event.arguments[0]
            output += '$c was kicked from '
            output += escape(event.target)
            output += ' by '
            output += event.source.split('!')[0]
            output += ' $c14[$c'
            output += event.arguments[1]
            output += '$c14]$c'

        elif event.type in ['join', ]:
            # we get an in event for joining chans, so ignore out
            if event.direction == 'out':
                return
            targets.append(event.target)
            output += '$c6-$c!$c6-$b$c10 '
            output += event.source.split('!')[0]
            output += '$b $c14[$c10'
            output += escape(event.source.split('!')[1])
            output += '$c14]$c '
            output += 'has joined $b'
            output += escape(event.target)

        elif event.type in ['nick', ]:
            output += '$c6-$c!$c6-$c10 '
            output += event.source.split('!')[0]
            output += '$c is now known as $c10'
            output += str(event.target)

        elif event.type in ['currenttopic', ]:
            targets.append(event.arguments[0])
            output += '$c6-$c!$c6-$c10 Topic for $c10'
            output += event.arguments[0]
            output += '$c: '
            output += event.arguments[1]

        elif event.type in ['quit', ]:
            output += '$c6-$c!$c6-$c10 '
            output += event.source.split('!')[0]
            output += ' $c14[$c'
            output += escape(event.source.split('!')[1])
            output += '$c14]$c has quit $c14[$c'
            output += event.arguments[0]
            output += '$c14]$c'

        elif event.type in ['ctcp', ] and event.arguments[0] == 'ACTION':
            return

        elif event.type in ['ping', 'pong', ]:
            return

        elif event.type in ['cap', ]:
            if event.direction == 'out':
                if event.target[0].upper() == 'REQ':
                    output += 'IRCv3 CAP Requested by Client: {}'.format(' '.join(event.target[1:]))
                else:
                    return  # end, so ignore

            if event.direction == 'in':
                if event.arguments[0].upper() == 'ACK':
                    output += 'IRCv3 CAP Enabled by Server: {}'.format(' '.join(event.arguments[1:]))

        else:
            targets.append('tofix')
            output += str(event.direction) + ' ' + str(event.type) + ' ' + escape(str(event.source)) + ' ' + escape(str(event.target)) + ' ' + escape(str(event.arguments))

        # # TODO: make this a bool debug option
        # debugmsg = [event.direction, event.type, event.source, event.target, event.arguments]
        # self.bot.gui.put_line(escape(str(debugmsg)))

        self.bot.gui.put_line(display_unescape(output + '$r'))  # +$r because that means reset
        self.log(output, event.server, targets)

    def log(self, output, server='global', targets=['global']):
        server_escape = filename_escape(server)
        targets_escape = []
        for target in targets:
            targets_escape.append(filename_escape(target))
        for target in targets_escape:
            if not os.path.exists('logs'):
                os.makedirs('logs')
            if not os.path.exists('logs/{}'.format(server)):
                os.makedirs('logs/{}'.format(server))
            path = 'logs/{}.{}.log'.format(server_escape, target)

            if target not in self.logfiles_open or not os.path.exists(path):
                output = '$c14 Logfile Opened - ' + strftime('%A %B %d, %H:%M:%S %Y', localtime()) + '\n' + output
                self.logfiles_open[target] = strftime('%A %B %d', localtime())
            elif self.logfiles_open[target] != strftime('%A %B %d', localtime()):
                output = '$c14 New Day - ' + strftime('%A %B %d, %H:%M:%S %Y', localtime()) + '\n' + output
                self.logfiles_open[target] = strftime('%A %B %d', localtime())

            outfile = open(path.lower(), 'a', encoding='utf-8')
            outfile.write(unescape(output) + '\n')
            outfile.close()

    def nick_color(self, nickhost):
        nick = nickhost.split('!')[0]
        if nick not in self.nick_colors:
            self.nick_colors[nick] = random.randint(2, 13)
        return '$c' + str(self.nick_colors[nick]) + nick


def hide_pw_if_necessary(msg, command_char="'"):
    """If a password message is in the input string, hide it in the output."""
    msg_parts = msg.split()
    if len(msg_parts):
        command = msg_parts[0].lower()
    else:
        command = ''

    if command == '{}login'.format(command_char):
        if len(msg_parts) > 2:
            msg_parts[2] = '******'
    elif command == '{}register'.format(command_char):
        if len(msg_parts) > 2:
            msg_parts[2] = '******'

    return ' '.join(msg_parts)


# TODO: this function needs to support ${$} format
def display_unescape(in_str):
    in_str = in_str.replace('${$}', '$$')
    output = ''
    while in_str != '':
        if in_str[0] == '$':
            if len(in_str) > 1 and in_str[1] == '$':
                in_str = in_str[2:]
                output += '$'
            elif len(in_str) > 1 and in_str[1] == 'c':
                fore = ''
                back = ''
                in_str = in_str[2:]
                in_fore = True

                while True:
                    if len(in_str) > 0 and in_str[0].isdigit():
                        digit = in_str[0]
                        in_str = in_str[1:]

                        if in_fore:
                            if len(fore) < 2:
                                fore += digit
                            else:
                                in_str = digit + in_str
                                break
                        else:
                            if len(back) < 2:
                                back += digit
                            else:
                                in_str = digit + in_str
                                break

                    elif len(in_str) > 0 and in_str[0] == ',':
                        if in_fore:
                            in_str = in_str[1:]
                            in_fore = False
                        else:
                            break

                    else:
                        break

                if fore != '':
                    if int(fore) > 15:
                        while int(fore) > 15:
                            fore = str(int(fore) - 14)
                    output += fore_colors[str(int(fore))]
                    if back != '':
                        if int(back) > 15:
                            while int(back) > 15:
                                back = str(int(back) - 14)
                        output += back_colors[str(int(back))]

                else:
                    output += colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.NORMAL

            elif len(in_str) > 1 and in_str[1] == 'r':
                output += colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.NORMAL
                in_str = in_str[2:]

            elif len(in_str) > 1 and in_str[1] in ['b', 'i', 'u']:
                in_str = in_str[2:]

            elif len(in_str) >= 2:
                in_str = in_str[2:]

        elif len(in_str) > 0:
            output += in_str[0]
            if len(in_str) > 0:
                in_str = in_str[1:]

        else:
            break

    return output

fore_colors = {
    '0': colorama.Fore.WHITE + colorama.Style.NORMAL,
    '1': colorama.Fore.BLACK + colorama.Style.NORMAL,
    '2': colorama.Fore.BLUE + colorama.Style.NORMAL,
    '3': colorama.Fore.GREEN + colorama.Style.NORMAL,
    '4': colorama.Fore.RED + colorama.Style.BRIGHT,
    '5': colorama.Fore.RED + colorama.Style.NORMAL,
    '6': colorama.Fore.MAGENTA + colorama.Style.NORMAL,
    '7': colorama.Fore.YELLOW + colorama.Style.NORMAL,
    '8': colorama.Fore.YELLOW + colorama.Style.BRIGHT,
    '9': colorama.Fore.GREEN + colorama.Style.BRIGHT,
    '10': colorama.Fore.CYAN + colorama.Style.NORMAL,
    '11': colorama.Fore.CYAN + colorama.Style.BRIGHT,
    '12': colorama.Fore.BLUE + colorama.Style.BRIGHT,
    '13': colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
    '14': colorama.Fore.BLACK + colorama.Style.BRIGHT,
    '15': colorama.Fore.WHITE + colorama.Style.NORMAL,
}

bold_fore_colors = {
    '0': colorama.Fore.WHITE + colorama.Style.BRIGHT,
    '1': colorama.Fore.BLACK + colorama.Style.DIM,
    '2': colorama.Fore.BLUE + colorama.Style.NORMAL,
    '3': colorama.Fore.GREEN + colorama.Style.NORMAL,
    '4': colorama.Fore.RED + colorama.Style.BRIGHT,
    '5': colorama.Fore.RED + colorama.Style.NORMAL,
    '6': colorama.Fore.MAGENTA + colorama.Style.NORMAL,
    '7': colorama.Fore.YELLOW + colorama.Style.NORMAL,
    '8': colorama.Fore.YELLOW + colorama.Style.BRIGHT,
    '9': colorama.Fore.GREEN + colorama.Style.BRIGHT,
    '10': colorama.Fore.CYAN + colorama.Style.NORMAL,
    '11': colorama.Fore.CYAN + colorama.Style.BRIGHT,
    '12': colorama.Fore.BLUE + colorama.Style.BRIGHT,
    '13': colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
    '14': colorama.Fore.BLACK + colorama.Style.BRIGHT,
    '15': colorama.Fore.WHITE + colorama.Style.BRIGHT,
}

back_colors = {
    '0': '',
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': '',
    '6': '',
    '7': '',
    '8': '',
    '9': '',
    '10': '',
    '11': '',
    '12': '',
    '13': '',
    '14': '',
    '15': '',
}
