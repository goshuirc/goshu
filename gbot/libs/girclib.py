#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import bisect
import ssl
import irc, irc.client, irc.modes


class IRC:
    """Wrapper for irclib's IRC class."""

    def __init__(self):
        self.irc = irc.client.IRC()

        self.servers = {}  # server connections
        self.connections = []  # dcc connections
        self.handlers = {
            'in' : {},
            'out' : {},
            'all' : {},
        }

        self.irc.add_global_handler('all_events', self._handle_irclib)
        self.irc.remove_global_handler('irc', irc.client._ping_ponger)
        self.add_handler('in', 'ping', self._handle_ping, -42)

    # Servers
    def server(self, name):
        connection = ServerConnection(name, self)
        self.servers[name] = connection
        return connection

    def dcc(self, dcctype="chat"):
        c = irc.client.DCCConnection(dcctype)
        self.connections.append(c)
        return c

    def name(self, connection):
        """Given connection, return server name."""
        for server in self.servers:
            if self.servers[server].connection == connection:
                return server

    # Processing
    def process_once(self, timeout=0):
        self.irc.process_once(timeout)

    def process_forever(self, timeout=0.2):
        self.irc.process_forever(timeout)

    # Handling
    def add_handler(self, direction, event, handler, priority=0):
        if not event in self.handlers[direction]:
            self.handlers[direction][event] = []
        bisect.insort(self.handlers[direction][event], ((priority, handler)))

    def remove_handler(self, direction, event, handler):
        if not event in self.handlers[direction]:
            return 0
        for h in self.handlers[direction][event]:
            if handler == h[1]:
                self.handlers[direction][event].remove(h)

    def _handle_irclib(self, connection, event):
        if event.type in ['privmsg', 'pubmsg', 'privnotice', 'pubnotice', 'action', 'currenttopic',
                                 'motd', 'endofmotd', 'yourhost', 'endofnames', 'ctcp', 'topic', 'quit',
                                 'part', 'kick', 'kick', 'join', ]:
            event_arguments = []
            for arg in event.arguments:
                event_arguments.append(escape(arg))
        else:
            event_arguments = event.arguments
            #event_arguments = []
            #for arg in event.arguments():
            #    event_arguments.append(escape(arg))
        #if 'raw' not in event.eventtype():
        #    print("    ", event.eventtype(), ' ', str(event_arguments))
        new_event = Event(self, self.name(connection), 'in', event.type, event.source, event.target, event_arguments)
        self._handle_event(new_event)

    def _handle_event(self, event):
        """Call handle functions, and all that fun stuff."""
        self.servers[event.server].update_info(event)
        called = []
        for event_direction in [event.direction, 'all']:
            for event_type in [event.type, 'all']:
                if event_type in self.handlers[event_direction]:
                    for h in self.handlers[event_direction][event_type]:
                        if h[1] not in called:
                            called.append(h[1])
                            h[1](event)

    def _handle_ping(self, event):
        self.servers[event.server].pong(event.arguments[0])

    # Disconnect
    def disconnect_all(self, message):
        for name in self.servers.copy():
            self.servers[name].connection.disconnect(message)
            del self.servers[name]


class ServerConnection:
    """IRC Server Connection."""

    def __init__(self, name, irc):
        self.name = name
        self.irc = irc
        self.info = {
            'name' : name,
            'connection' : {},
            'channels' : {},
            'users' : {},
        }

    # Connection
    def connect(self, address, port, nick, password=None, username=None, ircname=None, localaddress="", localport=0, sslsock=False, ipv6=False):
        self.connection = self.irc.irc.server()
        self.info['connection'] = {
            'address' : address,
            'port' : port,
            'nick' : nick,
        }
        if password != None:
            self.info['connection']['password'] = password
        if username != None:
            self.info['connection']['username'] = username
        if ircname != None:
            self.info['connection']['ircname'] = ircname
        if localaddress != "":
            self.info['connection']['localaddress'] = localaddress
        if localport != 0 or localaddress != "":
            self.info['connection']['localport'] = localport
        if sslsock != False:
            self.info['connection']['sslsock'] = sslsock
        if ipv6 != False:
            self.info['connection']['ipv6'] = ipv6

        if sslsock:
            Factory = irc.connection.Factory(wrapper=ssl.wrap_socket, ipv6=ipv6)
        else:
            Factory = irc.connection.Factory(ipv6=ipv6)

        self.connection.connect(address, port, nick, password, username, ircname, Factory)
        self.connection.buffer.errors = 'replace'

    def disconnect(self, message):
        self.info = {
            'connection' : {},
            'channels' : {},
            'users' : {},
        }
        self.connection.disconnect(message)
        del self.connection

    # IRC Commands
    def action(self, target, action):
        self.connection.action(target, unescape(action))
        self.irc._handle_event(Event(self.irc, self.name, 'out', 'action', self.info['connection']['nick'], target, [action]))

    def admin(self, server=''):
        self.connection.admin(server)
        self.irc._handle_event(Event(self.irc, self.name, 'out', 'admin', self.info['connection']['nick'], server))

    def ctcp(self, type, target, string):
        self.connection.ctcp(type, target, string)
        if len(string.split()) > 1:
            (ctcp_type, ctcp_args) = string.split(' ', 1)
        else:
            (ctcp_type, ctcp_args) = (string, '')
        self.irc._handle_event(Event(self.irc, self.name, 'out', 'ctcp', self.info['connection']['nick'], target, [ctcp_type, ctcp_args]))

    def ctcp_reply(self, ip, string):
        self.connection.ctcp_reply(ip, string)
        if len(string.split()) > 1:
            (ctcp_type, ctcp_args) = string.split(' ', 1)
        else:
            (ctcp_type, ctcp_args) = (string, '')
        self.irc._handle_event(Event(self.irc, self.name, 'out', 'ctcp_reply', self.info['connection']['nick'], ip, [ctcp_type, ctcp_args]))

    def join(self, channel, key=''):
        self.connection.join(channel, key)
        #self.irc._handle_event(Event(self.irc, self.name, 'out', 'join', self.info['connection']['nick'], channel, [key]))

    def pong(self, target):
        self.connection.pong(target)
        self.irc._handle_event(Event(self.irc, self.name, 'out', 'pong', self.info['connection']['nick'], target))

    def privmsg(self, target, message, chanserv_escape=True):
        if irc.client.is_channel(target):
            command = 'pubmsg'
            if chanserv_escape and message[0] == '.':
                message_escaped = message[0]
                message_escaped += '/b/b'
                message_escaped += message[1:]
                message = message_escaped
        else:
            command = 'privmsg'

        self.connection.privmsg(target, unescape(message))
        self.irc._handle_event(Event(self.irc, self.name, 'out', command, self.info['connection']['nick'], target, [message]))

    # Internal book-keeping
    def update_info(self, event):
        if event.type == 'join':
            self.create_user(event.source)
            self.create_channel(event.target)
            self.info['channels'][event.target]['users'][event.source.split('!')[0]] = ''

        elif event.type == 'namreply':
            # only create new dict if it doesn't exist, bakabaka
            if 'users' not in self.info['channels'][event.arguments[1]]:
                self.info['channels'][event.arguments[1]]['users'] = {}
            for user in event.arguments[2].split():
                if user[0] in '+%@&~':
                    user_priv = user[0]
                    user_nick = user[1:]
                else:
                    user_nick = user
                    user_priv = ''
                self.create_user(user_nick)
                self.info['channels'][event.arguments[1]]['users'][user_nick] = user_priv

        elif event.type == 'currenttopic':
            self.create_channel(event.arguments[0])
            self.info['channels'][event.arguments[0]]['topic']['topic'] = event.arguments[1]

        elif event.type == 'topicinfo':
            self.create_channel(event.arguments[0])
            self.info['channels'][event.arguments[0]]['topic']['user'] = event.arguments[1]
            self.info['channels'][event.arguments[0]]['topic']['time'] = event.arguments[2]

        elif event.type == 'nick':
            for channel in self.info['channels'].copy():
                if event.source.split('!')[0] in self.info['channels'][channel]['users']:
                    self.info['channels'][channel]['users'][event.target] = self.info['channels'][channel]['users'][event.source.split('!')[0]]
                    del self.info['channels'][channel]['users'][event.source.split('!')[0]]
            self.info['users'][event.target] = self.info['users'][event.source.split('!')[0]]
            del self.info['users'][event.source.split('!')[0]]

        elif event.type == 'part':
            try:
                del self.info['channels'][event.target]['users'][event.source.split('!')[0]]
            except:
                ...

        elif event.type == 'kick':
            try:
                del self.info['channels'][event.target]['users'][event.arguments[0]]
            except:
                ...

        elif event.type == 'quit':
            for channel in self.info['channels']:
                if event.source.split('!')[0] in self.info['channels'][channel]['users']:
                    del self.info['channels'][channel]['users'][event.source.split('!')[0]]
            del self.info['users'][event.source.split('!')[0]]

        elif event.type == 'mode':
            # todo: channel modes, and user-only modes. Automagically populate mode tables from server join info
            for mode in irc.modes._parse_modes(" ".join(event.arguments), "bklvohaq"):
                if mode[1] not in mode_dict:
                    continue

                if mode[0] == '-':
                    if mode_dict[mode[1]] in self.info['channels'][event.target]['users'][mode[2]]:
                        self.info['channels'][event.target]['users'][mode[2]] = self.info['channels'][event.target]['users'][mode[2]].replace(mode_dict[mode[1]], '')
                elif mode[0] == '+':
                    if mode_dict[mode[1]] not in self.info['channels'][event.target]['users'][mode[2]]:
                        self.info['channels'][event.target]['users'][mode[2]] += mode_dict[mode[1]]

    def create_user(self, user):
        user_nick = user.split('!')[0]
        #user_host = user.split('@')[1]
        #user_uname = user.split('!')[1].split('@')[0]
        if user_nick not in self.info['users']:
            self.info['users'][user_nick] = {}

    def create_channel(self, channel):
        if channel not in self.info['channels']:
            self.info['channels'][channel] = {
                'topic' : {},
                'users' : {}
            }


class Event:
    """IRC Event."""

    def __init__(self, irc, server, direction, type, source, target, arguments=None):
        self.server = server
        self.direction = direction
        self.type = type
        self.source = source
        self.target = target
        if arguments:
            self.arguments = arguments
        else:
            self.arguments = []
        if direction == 'in':
            if target == irc.servers[server].info['connection']['nick']:
                self.from_to = str(source).split('!')[0]
            else:
                self.from_to = str(target).split('!')[0]
        else:
            self.from_to = str(target).split('!')[0]


unescape_dict = {
    '/' : '/',  # unescape real slashes
    'b' : '\x02',  # bold
    'c' : '\x03',  # color
    'i' : '\x1d',  # italic
    'u' : '\x1f',  # underline
    'r' : '\x0f',  # reset
}


def escape(string):
    """Change IRC codes into goshu codes."""
    string = string.replace('/', '//')  # escape real slashes
    string = string.replace('\x02', '/b')  # bold
    string = string.replace('\x03', '/c')  # color
    string = string.replace('\x1d', '/i')  # italic
    string = string.replace('\x1f', '/u')  # underline
    string = string.replace('\x0f', '/r')  # reset
    return string


def unescape(in_string):
    """Change goshu codes into IRC codes."""
    if len(in_string) < 1:
        return ''
    out_string = ''
    while 1:
        if in_string[0] == '/':
            if len(in_string) < 2:
                break
            if in_string[1] in unescape_dict:
                out_string += unescape_dict[in_string[1]]
            else:
                out_string += in_string[0] + '?' + in_string[1] + '?'
            in_string = in_string[2:]
        else:
            out_string += in_string[0]
            in_string = in_string[1:]
        if len(in_string) < 1:
            break
    return out_string

# todo: Automatically populate this from server join info
mode_dict = {
    'v' : '+',  # voice
    'h' : '%',  # hop
    'o' : '@',  # op
    'a' : '&',  # protected
    'q' : '~'   # owner
}


class NickMask(irc.client.NickMask):
    ...


def is_channel(name):
    return irc.client.is_channel(name)


def remove_control_codes(line):
    new_line = ''
    while len(line) > 0:
        try:
            if line[0] == '/':
                line = line[1:]

                if line[0] == '/':
                    new_line += '/'
                    line = line[1:]

                elif line[0] == 'c':
                    line = line[1:]
                    if line[0].isdigit():
                        line = line[1:]
                        if line[0].isdigit():
                            line = line[1:]
                            if line[0] == ',':
                                line = line[1:]
                                if line[0].isdigit():
                                    line = line[1:]
                                    if line[0].isdigit():
                                        line = line[1:]

                #elif line[0] in ['b', 'i', 'u', 'r']:
                #    line = line[1:]

                else:
                    line = line[1:]

            else:
                new_line += line[0]
                line = line[1:]
        except IndexError:
            ...
    return new_line
