#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
from gbot.libs.girclib import unescape


class invite(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'addchan': [self.addchan, "--- add the currently joined channel to our autojoin list"],
                'remchan': [self.remchan, "--- remove the currently joined channel from our autojoin list"],
            },
            'in': {
                'invite': [(0, self.invite)],
            },
        }

    def invite(self, event):
        """When someone /invites us, join the channel."""
        self.bot.irc.servers[event.server].join(event.arguments[0])
        self.bot.irc.servers[event.server].privmsg(event.arguments[0], 'Thanks for inviting me, {nick}. To keep me in here, use the command:   {pre}addchan'.format(nick=event.source.split('!')[0], pre=self.bot.settings.store['prefix']))

    def addchan(self, event, command, usercommand):
        """Add the current channel to our autojoin list."""
        if event.target not in self.bot.irc.servers[event.server].info['channels']:
            self.bot.irc.msg(event, 'Sorry, this command can only be used in a channel, by a channel operator')
            return

        user_privs = self.bot.irc.servers[event.server].info['channels'][event.target]['users'].get(event.source.nick, '')
        is_prived = self.bot.irc.servers[event.server].is_prived(user_privs, 'o')  # is an operator

        if not is_prived:
            self.bot.irc.msg(event, 'Sorry, you need to be a channel operator to do this')
            return

        if 'autojoin_channels' not in self.bot.info.store[event.server]['connection']:
            self.bot.info.store[event.server]['connection']['autojoin_channels'] = []

        if unescape(event.target) not in self.bot.info.store[event.server]['connection']['autojoin_channels']:
            self.bot.info.store[event.server]['connection']['autojoin_channels'].append(unescape(event.target))
            self.bot.info.save()

        self.bot.irc.msg(event, 'Added this channel to my autojoin list! To remove:  {pre}remchan'.format(pre=self.bot.settings.store['prefix']), 'public')

    def remchan(self, event, command, usercommand):
        """Remove the current channel from our autojoin list."""
        if event.target not in self.bot.irc.servers[event.server].info['channels']:
            self.bot.irc.msg(event, 'Sorry, this command can only be used in a channel, by a channel operator')
            return

        user_privs = self.bot.irc.servers[event.server].info['channels'][event.target]['users'].get(event.source.nick, '')
        is_prived = self.bot.irc.servers[event.server].is_prived(user_privs, 'o')  # is an operator

        if not is_prived:
            self.bot.irc.msg(event, 'Sorry, you need to be a channel operator to do this')
            return

        if 'autojoin_channels' not in self.bot.info.store[event.server]['connection']:
            self.bot.info.store[event.server]['connection']['autojoin_channels'] = []

        if unescape(event.target) in self.bot.info.store[event.server]['connection']['autojoin_channels']:
            self.bot.info.store[event.server]['connection']['autojoin_channels'].remove(unescape(event.target))
            self.bot.info.save()

        self.bot.irc.msg(event, 'Removed this channel from my autojoin list! To readd:  {pre}addchan'.format(pre=self.bot.settings.store['prefix']), 'public')
