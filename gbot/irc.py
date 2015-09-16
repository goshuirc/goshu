#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import socket

import girc

# default ping timeouts
timeout_check_interval = {
    'minutes': 3,
}
timeout_length = {
    'minutes': 6,
}


class IRC:
    """Manages goshubot's IRC communications."""

    def __init__(self, bot):
        self.r = girc.Reactor()
        self.bot = bot

        self.add_handler('in', 'kick', self._handle_kick)

        # debug
        self.add_handler('in', 'raw', self._handle_raw_in, priority=1)
        self.add_handler('out', 'raw', self._handle_raw_out, priority=1)

    # debug
    def _handle_raw_in(self, event):
        print(event['server'].name, ' ->', girc.formatting.escape(event['data']))

    def _handle_raw_out(self, event):
        print(event['server'].name, '<- ', girc.formatting.escape(event['data']))

    # add handlers
    def add_handler(self, direction, verb, child_fn, priority=10):
        self.r.register_event(direction, verb, child_fn, priority=priority)

    @property
    def servers(self):
        return self.r.servers

    def get_server(self, server):
        """Return a proper server connection."""
        if isinstance(server, girc.client.ServerConnection):
            return server
        elif isinstance(server, girc.types.Server):
            server_name = server.name
        elif isinstance(server, str):
            server_name = server
        else:
            raise Exception('`server` must be a server object or a name')

        return self.r.servers[server_name]

    def run_forever(self):
        """Run forever."""
        try:
            self.r.run_forever()
        except KeyboardInterrupt:
            self.r.shutdown('Goodbye')
            self.r.close()
        finally:
            self.r.close()

    def _handle_kick(self, event):
        user_nick = event['server'].istring(event['params'][0]).lower()
        our_nick = event['server'].nick.lower()
        channel = event['channel'].lower()

        if user_nick == our_nick:
            try:
                server_name = event['server'].name
                self.bot.info.store['servers'][server_name]['autojoin_channels'].remove(channel)
                self.bot.info.save()
            except:
                pass

    def connect_info(self, info, settings):
        """Set connect info given our info and settings."""
        default_nick = info.get('default_nick', None)
        server_dict = info.get('servers', {})
        for name, server in server_dict.items():
            kwargs = {}

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
                srv_username = server.get('connect_username', '*')

            srv_realname = None
            if server.get('srv_realname'):
                srv_realname = server.get('connect_realname', '*')

            local_address = ""
            if server.get('localaddress'):
                local_address = server.get('localaddress')
            local_port = server.get('localport', 0)

            if local_address and local_port:
                kwargs['local_addr'] = (local_address, local_port)

            srv_ssl = server.get('ssl', False)
            srv_ipv6 = server.get('ipv6', False)

            if srv_ipv6:
                family = socket.AF_INET6
            else:
                family = 0

            autojoin_channels = []
            if server.get('autojoin_channels'):
                autojoin_channels = server.get('autojoin_channels')

            # XXX - TODO: - use these
            wait_time = server.get('vhost_wait', 0)
            if wait_time:
                self.bot.gui.put_line('Waiting {} seconds to join channels. '
                                      'This can be changed in the connection configuration.'
                                      ''.format(wait_time))

            srv_timeout_check = server.get('timeout_check_interval', timeout_check_interval)
            srv_timeout_length = server.get('timeout_length', timeout_length)

            # nickserv
            nickserv_serv_nick = server.get('nickserv_serv_nick', 'NickServ')
            nickserv_password = server.get('nickserv_password', None)

            # connect
            server = self.r.create_server(name)
            if srv_password:
                server.set_connect_password(srv_password)
            server.set_user_info(srv_nick, user=srv_username, real=srv_realname)
            server.join_channels(*autojoin_channels)
            server.connect(srv_host, srv_port, ssl=srv_ssl, family=family, **kwargs)
