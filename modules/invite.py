#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.girclib import unescape


class invite(Module):
    """Handles joining invited channels, and allowing chanops to ask goshu to autojoin their channel!"""

    def invite_listener(self, event):
        """When someone /invites us, join the channel

        @listen in invite
        """
        self.bot.irc.servers[event.server].join(event.arguments[0])
        self.bot.irc.servers[event.server].privmsg(event.arguments[0], 'Thanks for inviting me, {nick}. To keep me in here, use the command:   {pre}addchan'.format(nick=event.source.split('!')[0], pre=self.bot.settings.store['command_prefix']))

    def cmd_addchan(self, event, command, usercommand):
        """Add the currently joined channel to our autojoin list"""
        if event.target not in self.bot.irc.servers[event.server].info['channels']:
            self.bot.irc.msg(event, 'Sorry, this command can only be used in a channel, by a channel operator')
            return

        user_privs = self.bot.irc.servers[event.server].info['channels'][event.target]['users'].get(event.source.nick, '')
        is_prived = self.bot.irc.servers[event.server].is_prived(user_privs, 'o')  # is an operator

        if not is_prived:
            self.bot.irc.msg(event, 'Sorry, you need to be a channel operator to do this')
            return

        if 'autojoin_channels' not in self.bot.info.get(event.server, {}):
            server_dict = self.bot.info.get(event.server, {})
            server_dict['autojoin_channels'] = []
            self.bot.info.set(event.server, server_dict)

        if unescape(event.target.lower()) not in self.bot.info.get(event.server, {})['autojoin_channels']:
            server_dict = self.bot.info.get(event.server, {})
            server_dict['autojoin_channels'].append(unescape(event.target.lower()))
            self.bot.info.set(event.server, server_dict)
            self.bot.info.save()

        self.bot.irc.msg(event, 'Added this channel to my autojoin list! To remove:  {pre}remchan'.format(pre=self.bot.settings.store['command_prefix']), 'public')

    def cmd_remchan(self, event, command, usercommand):
        """Remove the currently joined channel from our autojoin list"""
        if event.target not in self.bot.irc.servers[event.server].info['channels']:
            self.bot.irc.msg(event, 'Sorry, this command can only be used in a channel, by a channel operator')
            return

        user_privs = self.bot.irc.servers[event.server].info['channels'][event.target]['users'].get(event.source.nick, '')
        is_prived = self.bot.irc.servers[event.server].is_prived(user_privs, 'o')  # is an operator

        if not is_prived:
            self.bot.irc.msg(event, 'Sorry, you need to be a channel operator to do this')
            return

        if 'autojoin_channels' not in self.bot.info.get(event.server, {}):
            server_dict = self.bot.info.get(event.server, {})
            server_dict['autojoin_channels'] = []
            self.bot.info.set(event.server, server_dict)

        if unescape(event.target.lower()) in self.bot.info.get(event.server, {})['autojoin_channels']:
            server_dict = self.bot.info.get(event.server, {})
            server_dict['autojoin_channels'].remove(unescape(event.target.lower()))
            self.bot.info.set(event.server, server_dict)
            self.bot.info.save()

        self.bot.irc.msg(event, 'Removed this channel from my autojoin list! To readd:  {pre}addchan'.format(pre=self.bot.settings.store['command_prefix']), 'public')
