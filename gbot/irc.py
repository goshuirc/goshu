#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from .libs import girclib


class IRC(girclib.IRC):
    """Manages goshubot's IRC communications."""

    def __init__(self, bot):
        girclib.IRC.__init__(self)
        self.bot = bot

    def connect_info(self, info, settings):
        for name in info.store:
            try:
                srv_nick = info.store[name]['connection']['nick']
            except KeyError:
                srv_nick = settings.store['nick']

            srv_address = info.store[name]['connection']['address']
            srv_port = info.store[name]['connection']['port']

            try:
                srv_password = info.store[name]['connection']['password']
            except KeyError:
                srv_password = None

            try:
                srv_username = info.store[name]['connection']['username']
            except:
                srv_username = None

            try:
                srv_ircname = info.store[name]['connection']['ircname']
            except:
                srv_ircname = None

            try:
                srv_localaddress = info.store[name]['connection']['localaddress']
                srv_localport = info.store[name]['connection']['localport']
            except:
                srv_localaddress = ""
                srv_localport = 0

            try:
                srv_ssl = info.store[name]['connection']['ssl']
            except:
                srv_ssl = False

            try:
                srv_ipv6 = info.store[name]['connection']['ipv6']
            except:
                srv_ipv6 = False

            # autojoin channels
            wait_time = 5
            if 'vhost_wait' in info.store[name]['connection']:
                wait_time = int(info.store[name]['connection']['vhost_wait'])
            self.bot.gui.put_line('Waiting {} seconds to join channels. To change this, set the connection:vhost_wait setting for this server.'.format(wait_time))

            autojoin_channels = []
            if 'autojoin_channels' in info.store[name]['connection']:
                autojoin_channels = info.store[name]['connection']['autojoin_channels']

            # timeout
            try:
                timeout_check_interval = info.store[name]['connection']['timeout_check_interval']
            except:
                timeout_check_interval = girclib.timeout_check_interval

            try:
                timeout_length = info.store[name]['connection']['timeout_length']
            except:
                timeout_length = girclib.timeout_length

            # server creation
            s = self.server(name, timeout_check_interval=timeout_check_interval, timeout_length=timeout_length)
            s.connect(srv_address, srv_port, srv_nick, srv_password, srv_username, srv_ircname, srv_localaddress, srv_localport, srv_ssl, srv_ipv6, autojoin_channels=autojoin_channels, wait_time=wait_time)

            if 'nickserv_password' in info.store[name]['connection']:
                s.privmsg('nickserv', 'identify ' + info.store[name]['connection']['nickserv_password'])

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
    if zone is 'public':
        target = event.from_to
    elif zone is 'dcc':
        # skip to below for now, will handle actual dcc later
        if strict:
            zone = 'private'
        else:
            return None

    if zone is 'private':
        if girclib.is_channel(event.source):
            target = event.source
        else:
            target = event.source.split('!')[0]
    return target
