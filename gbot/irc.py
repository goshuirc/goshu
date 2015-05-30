#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from .libs import girclib


class IRC(girclib.IRC):
    """Manages goshubot's IRC communications."""

    def __init__(self, bot):
        girclib.IRC.__init__(self)
        self.bot = bot

        self.add_handler('in', 'kick', self._handle_kick)

    def _handle_kick(self, event):
        user_nick = self.servers[event.server].istring(event.arguments[0]).lower()
        our_nick = self.servers[event.server].istring(self.servers[event.server].info['connection']['nick']).lower()
        channel = event.target.lower()

        if user_nick == our_nick:
            try:
                self.bot.info.store['servers'][self.servers[event.server].info['name']]['autojoin_channels'].remove(channel)
                self.bot.info.save()
            except:
                pass

    def connect_info(self, info, settings):
        default_nick = info.get('default_nick', None)
        server_dict = info.get('servers', {})
        for name, server in server_dict.items():
            srv_nick = server.get('nick')
            if not srv_nick:
                srv_nick = default_nick
            srv_host = server.get('hostname')
            srv_port = server.get('port')

            srv_password = None
            if server.get('connect_password'):
                srv_password = server.get('connect_password')

            srv_username = None
            if server.get('connect_username'):
                srv_username = server.get('connect_username')

            srv_realname = None
            if server.get('srv_realname'):
                srv_realname = server.get('realname')

            local_address = ""
            if server.get('localaddress'):
                local_address = server.get('localaddress')
            local_port = server.get('localport', 0)

            srv_ssl = server.get('ssl', False)
            srv_ipv6 = server.get('ipv6', False)

            wait_time = server.get('vhost_wait', 0)
            if wait_time:
                self.bot.gui.put_line('Waiting {} seconds to join channels. This can be changed in the connection configuration.'.format(wait_time))

            autojoin_channels = []
            if server.get('autojoin_channels'):
                autojoin_channels = server.get('autojoin_channels')

            timeout_check_interval = server.get('timeout_check_interval', girclib.timeout_check_interval)
            timeout_length = server.get('timeout_length', girclib.timeout_length)

            # nickserv
            nickserv_serv_nick = server.get('nickserv_serv_nick', 'NickServ')
            nickserv_password = server.get('nickserv_password', None)

            # server creation
            s = self.server(name, timeout_check_interval=timeout_check_interval, timeout_length=timeout_length)
            s.connect(srv_host, srv_port, srv_nick, srv_password, srv_username, srv_realname,
                      local_address, local_port, srv_ssl, srv_ipv6,
                      autojoin_channels=autojoin_channels, wait_time=wait_time,
                      nickserv_serv_nick=nickserv_serv_nick, nickserv_password=nickserv_password)

    def action(self, event, message, zone='private'):
        """Automagically message someone. Zone can be public or private, for preferring channel or user."""
        target = get_target(event, zone)
        self.servers[event.server].action(target, message)

    def msg(self, event, message, zone='private', strict=False):
        """Automagically message someone. Zone can be public, private, or dcc, for preferring channel or user."""
        target = get_target(event, zone, strict)

        if target is None:
            return False

        self.servers[event.server].privmsg(target, message)
        return True


def get_target(event, zone, strict=False):
    """Return the target to msg/action given the event and zone.

    If dcc is requested but not avaliable and not strict, simply go to private instead.
    If dcc is not avaliable and strict, do not send and feturn False."""
    # sanity check
    if zone not in ['public', 'private', 'dcc']:
        return None

    if zone is 'public':
        target = event.from_to
    elif zone is 'dcc':
        # skip to below for now, will handle actual dcc later
        if strict:
            return None
        else:
            zone = 'private'

    if zone is 'private':
        if girclib.is_channel(event.source):
            target = event.source
        else:
            target = event.source.split('!')[0]
    return target
