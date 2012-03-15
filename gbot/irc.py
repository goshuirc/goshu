#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot	-	http://danneh.net/goshu

from .libs import girclib
import time

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

            if 'vhost_wait' in info.store[name]['connection']:
                time.sleep(info.store[name]['connection']['vhost_wait']) # waiting for vhost to get set, in seconds

            if 'autojoin_channels' in info.store[name]['connection']:
                for channel in info.store[name]['connection']['autojoin_channels']:
                    s.join(channel)
