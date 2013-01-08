#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from .libs import girclib
import time
import threading


class ChannelJoiner(threading.Thread):
    """Thread to async join the server's channels, to not pause the server for ages."""

    def __init__(self, server, name, channels, wait_time):
        threading.Thread.__init__(self, name='ChannelJoiner-'+name)

        self.server = server
        self.channels = channels
        self.wait_time = wait_time

    def run(self):
        time.sleep(self.wait_time)

        for channel in self.channels:
            self.server.join(channel)


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

            s = self.server(name)
            s.connect(srv_address, srv_port, srv_nick, srv_password, srv_username, srv_ircname, srv_localaddress, srv_localport, srv_ssl, srv_ipv6)

            if 'nickserv_password' in info.store[name]['connection']:
                s.privmsg('nickserv', 'identify '+info.store[name]['connection']['nickserv_password'])

            if 'autojoin_channels' in info.store[name]['connection']:
                wait_time = 0
                if 'vhost_wait' in info.store[name]['connection']:
                    wait_time = info.store[name]['connection']['vhost_wait']

                ChannelJoiner(s, name, info.store[name]['connection']['autojoin_channels'], wait_time).start()

    def action(self, event, message, zone='private'):
        """Automagically message someone. Zone can be public or private, for preferring channel or user."""
        target = get_target(event, zone)
        self.servers[event.server].action(target, message)

    def msg(self, event, message, zone='private'):
        """Automagically message someone. Zone can be public or private, for preferring channel or user."""
        target = get_target(event, zone)
        self.servers[event.server].privmsg(target, message)


def get_target(event, zone):
    """Return the target to msg/action given the event and zone."""
    if zone is 'public':
        target = event.from_to
    else:
        if girclib.is_channel(event.source):
            target = event.source
        else:
            target = event.source.split('!')[0]
    return target
