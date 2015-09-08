#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from time import strftime, localtime
import datetime
import os
import random

from girc.formatting import escape, unescape
import colorama

from gbot.libs.helper import filename_escape
from gbot.modules import Module

colorama.init()


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

        @listen both all highest inline
        @listen both raw highest inline
        """
        if event['verb'] == 'raw':
            output = event['server'].name
            if event['direction'] == 'in':
                output += '  -> '
            else:
                output += ' <-  '
            output += event['raw']
            return

        # > 15:26:43
        output = '$c14'
        output += strftime('%H:%M:%S', localtime())

        # > -rizon-
        output += ' $c12-$c'
        output += event['server'].name
        output += '$c12-$c '

        targets = ['all']

        if event['verb'] == '':
            ...

        elif event['verb'] in ['welcome', 'yourhost', 'features', 'created', 'myinfo',
                               'yourid', 'luserclient', 'luserop', 'luserchannels',
                               'luserme', 'localusers', 'globalusers', 'motd', 'nomotd']:
            output += escape(' '.join(event['params'][1:]))

        elif event['verb'] == 'user':
            output += 'Your user info is: '
            output += escape(' '.join([x if x else '' for x in event['params']]))

        elif event['verb'] in ['privnotice', ]:
            targets.append(event['source'].name)
            output += '$c14-'
            output += '$c13' + event['source'].name
            try:
                output += '$c14($c13'
                if event['source'].is_user:
                    output += escape(event['source'].userhost)
                elif event['source'].is_server:
                    output += 'server'
                else:
                    output += 'unknown'
                output += '$c14)'
            except IndexError:
                output = output[:-1]
            output += '-$c '
            output += event['message']

        elif event['verb'] in ['cannotsendtochan', ]:
            chan = escape(event['channel'].name)
            msg = event['reason']
            targets.append(chan)

            output += '$c3-$c'
            output += escape(chan)
            output += '$c3- '
            output += '$r$b** $c4Message Rejected$r: '
            output += msg

        elif event['verb'] in ['nosuchservice', ]:
            service = escape(event['target'].nick)
            msg = event['message']
            targets.append(service)

            output += '$c3-$c'
            output += escape(service)
            output += '$c3- '
            output += '$r$b** $c4'
            output += msg

        elif event['verb'] in ['pubmsg', ]:
            targets.append(event['target'].name)
            output += '$c3-$c'
            output += escape(event['target'].name)
            output += '$c3- '
            output += '$c14<$c'

            selected_mode = ''
            user_nick = event['source'].nick

            if len(event['target'].prefixes[user_nick]):
                selected_mode = event['target'].prefixes[user_nick][0]
                output += escape(selected_mode)
            else:
                output += ' '

            output += self.nick_color(event['source'].nick)
            output += '$c14>$c '
            output += hide_pw_if_necessary(event['message'],
                                           self.bot.settings.store['command_prefix'])

        elif event['verb'] in ['pubnotice', ]:
            targets.append(event['target'].name)
            output += '$c3-$c'
            output += escape(event['target'].name)
            output += '$c3- '
            output += '$c[green]Notice$c -> '

            selected_mode = ''
            user_nick = event['source'].nick

            if len(event['target'].prefixes[user_nick]):
                selected_mode = event['target'].prefixes[user_nick][0]
                output += escape(selected_mode)
            else:
                output += ' '

            output += self.nick_color(event['source'].nick)
            output += '$r: '
            output += hide_pw_if_necessary(event['message'],
                                           self.bot.settings.store['command_prefix'])

        elif event['verb'] == 'ctcp':
            if event['direction'] == 'in':
                output += 'CTCP requested by $b'
                output += escape(event['source'].nick)
                output += '$b: $b'
                output += escape(event['ctcp_verb'].upper())
                output += '$b '
                output += event['ctcp_text']

            elif event['direction'] == 'out':
                output += 'CTCP query to $b'
                output += escape(event['target'].nick)
                output += '$b: $b'
                output += escape(event['ctcp_verb'].upper())
                output += '$b '
                output += event['ctcp_text']

        elif event['verb'] == 'ctcp_reply':
            if event['direction'] == 'in':
                output += 'CTCP reply from $b'
                output += escape(event['source'].nick)
                output += '$b: $b'
                output += escape(event['ctcp_verb'].upper())
                output += '$b '
                output += event['ctcp_text']

            elif event['direction'] == 'out':
                output += 'CTCP reply to $b'
                output += escape(event['target'].nick)
                output += '$b: $b'
                output += escape(event['ctcp_verb'].upper())
                output += '$b '
                output += event['ctcp_text']

        elif event['verb'] in ['privmsg', ]:
            output += '$c3-$c'
            if event['direction'] == 'in':
                output += escape(event['source'].nick)
                targets.append(escape(event['source'].nick))
            else:
                output += escape(event['target'].nick)
                targets.append(escape(event['target'].nick))
            output += '$c3- '
            output += '$c14<$c'
            output += self.nick_color(event['source'].nick)
            output += '$c14>$c '
            output += hide_pw_if_necessary(event['message'],
                                           self.bot.settings.store['command_prefix'])

        elif event['verb'] in ['action', ]:
            output += '$c3-$c'
            if event['direction'] == 'in':
                output += event['from_to'].name
                targets.append(event['from_to'].name)
            else:
                output += event['target'].name
                targets.append(event['target'].name)

            output += '$c3-$c  $b* '
            output += event['source'].nick + '$b '
            if len(event['message']):
                output += event['message']

        elif event['verb'] == 'umode':
            # we only care about incoming modes
            if event['direction'] == 'out':
                return

            output += 'Mode change '
            output += '$c14[$c'
            output += event['modestring']
            output += '$c14]$c'
            output += ' for user '
            output += event['target'].name

        elif event['verb'] == 'cmode':
            # we only care about incoming modes
            if event['direction'] == 'out':
                return

            targets.append(event['target'].name)
            output += '$c6-$c!$c6-$c '
            output += 'mode/'
            output += '$c10' + event['target'].name + ' '
            output += '$c14[$c'
            output += ' '.join(event['params'])
            output += '$c14]$c'
            output += ' by $b'
            output += event['source'].name

        elif event['verb'] in ['cmodeis', ]:
            chan = escape(event['channel'].name)

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'modes:'
            output += '$c10' + chan + ' '
            output += '$c14[$c'
            output += event['modestring']
            output += '$c14]$c'

        elif event['verb'] in ['chancreatetime', ]:
            chan = escape(event['channel'].name)
            timestamp = escape(event['timestamp'])

            try:
                created_ts = datetime.datetime.fromtimestamp(int(timestamp))
                created_ts = created_ts.strftime('%a, %d %b %Y %H:%M:%S')
            except:
                created_ts = '$r$b$c[red]MALFORMED TS:$r [' + timestamp + '$r]'

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'times:'
            output += '$c10' + chan + '$c '
            output += 'Channel created $b'
            output += created_ts

        elif event['verb'] in ['namreply', ]:
            chan = escape(event['channel'].name)
            nicks = escape(event.get('names'))

            targets.append(chan)
            output += '$c6-$c!$c6-$c '
            output += 'nicks:'
            output += '$c10' + chan + ' '
            output += '$c14[$c'
            output += nicks
            output += '$c14]$c'

        elif event['verb'] in ['endofnames', ]:
            chan = escape(event['channel'].name)
            user_dict = event['channel'].prefixes

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
                # XXX - TODO: - fix to work with isupport
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

        elif event['verb'] in ['kick', ]:
            targets.append(escape(event['channel'].name))
            output += '$c6-$c!$c6-$c10 '
            output += event['user'].nickmask,
            output += '$c was kicked from '
            output += escape(event['target'].name)
            output += ' by '
            output += event['source'].nick
            output += ' $c14[$c'
            output += event['message']
            output += '$c14]$c'

        elif event['verb'] in ['join', ]:
            # we get an in event for joining chans, so ignore out
            if event['direction'] == 'out':
                return
            [targets.append(escape(chan.name)) for chan in event['channels']]
            output += '$c6-$c!$c6-$c$b '
            output += event['source'].nick
            output += '$b $c14($c10'
            output += escape(event['source'].userhost)
            output += '$c14)$c '
            output += 'has joined $b'
            output += ', '.join([escape(chan.name) for chan in event['channels']])

        elif event['verb'] in ['nick', ]:
            output += '$c6-$c!$c6-$c10 '
            if event['source'] is None:
                output += '$cYou are now known as $c10'
            else:
                output += event['source'].nick
                output += '$c is now known as $c10'
            output += event['new_nick']

        elif event['verb'] in ['topic', ]:
            targets.append(escape(event['channel'].name))
            output += '$c6-$c!$c6-$c10 Topic for $c10'
            output += event['channel'].name
            output += '$c: '
            output += event['topic']

        elif event['verb'] in ['quit', ]:
            if event['direction'] == 'out':
                output += '$c6-$c!$c6-$c $b'
                output += event['server'].nick
                output += '$r$c[red] quit $c14[$c'
                output += event['message']
                output += '$c14]$c'
            else:
                output += '$c6-$c!$c6-$c $b'
                output += event['source'].nick
                output += ' $r$c14($c10'
                output += escape(event['source'].userhost)
                output += '$c14)$c[red] has quit $c14[$c'
                output += event['message']
                output += '$c14]$c'

        elif event['verb'] in ['ping', 'pong', ]:
            return

        elif event['verb'] in ['cap', ]:
            if event['direction'] == 'in':
                subcmd = event['params'][1].upper()

                if subcmd == 'LS':
                    output += 'Capabilities Supported by Server: {}'.format(event['params'][2])
                elif subcmd == 'ACK':
                    output += 'Capabilities Enabled by Server: {}'.format(event['params'][2])

            elif event['direction'] == 'out':
                subcmd = event['params'][0].upper()
                if subcmd == 'REQ':
                    output += 'Capabilities Requested by Client: {}'.format(event['params'][1])
                elif subcmd == 'END':
                    output += 'Capability Negotiation Ended by Client'
                elif subcmd == 'LS':
                    output += 'Requesting Server Capabilities'
                    if event['params']:
                        output += ' ('
                        output += ' '.join(event['params'][1:])
                        output += ')'
                else:
                    return  # ignore

        else:
            targets.append('tofix')
            output += str(event['direction']) + ' ' + str(event['verb']) + ' ' + escape(str(event['source'])) + ' ' + escape(str(event.get('target'))) + ' ' + escape(str(event['params']))

        # # TODO: make this a bool debug option
        # debugmsg = [event['direction'], event['verb'], event.source, event.target, event.arguments]
        # self.bot.gui.put_line(escape(str(debugmsg)))

        self.bot.gui.put_line(display_unescape(output + '$r'))  # +$r because that means reset
        self.log(output, event['server'].name, targets)

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
