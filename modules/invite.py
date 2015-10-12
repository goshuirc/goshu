#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from girc.formatting import unescape

from gbot.modules import Module


class invite(Module):
    """Handles getting invited to channels, and being asked to stay."""

    def invite_listener(self, event):
        """When someone /invites us, join the channel

        @listen in invite
        """
        event['server'].join_channel(event['channel'])
        event['source'].msg('Thanks for inviting me, {nick}. To keep me in here, '
                            'use the command:   {pre}addchan'
                            ''.format(nick=event.source.split('!')[0],
                                      pre=self.bot.settings.store['command_prefix']))

    def cmd_addchan(self, event, command, usercommand):
        """Add the currently joined channel to our autojoin list"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel, '
                                'by a channel operator')
            return

        if not event['target'].has_privs(event['source'], 'o'):
            event['source'].msg('Sorry, you need to be a channel operator to do this')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())

        if 'autojoin_channels' not in self.bot.info.store['servers'].get(server_name, {}):
            self.bot.info.store['servers'][server_name]['autojoin_channels'] = []

        if (channel_name not in
                self.bot.info.store['servers'][server_name]['autojoin_channels']):
            server_dict = self.bot.info.store['servers'][server_name]
            server_dict['autojoin_channels'].append(channel_name)
            self.bot.info.store['servers'][server_name] = server_dict
            self.bot.info.save()

        event['from_to'].msg("I'll now autojoin this channel! The command to remove me is:  "
                             "{p}remchan".format(p=self.bot.settings.store['command_prefix']))

    def cmd_remchan(self, event, command, usercommand):
        """Remove the currently joined channel from our autojoin list"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel, '
                                'by a channel operator')
            return

        if not event['target'].has_privs(event['source'], 'o'):
            event['source'].msg('Sorry, you need to be a channel operator to do this')
            return

        server_name = event['server'].name
        channel_name = event['target'].name.lower()

        if 'autojoin_channels' not in self.bot.info.store['servers'].get(server_name, {}):
            server_dict = self.bot.info.store['servers'].get(server_name, {})
            server_dict['autojoin_channels'] = []
            self.bot.info.store['servers'][server_name] = server_dict

        if (channel_name in
                self.bot.info.store['servers'].get(server_name, {})['autojoin_channels']):
            server_dict = self.bot.info.store['servers'].get(server_name, {})
            server_dict['autojoin_channels'].remove(channel_name)
            self.bot.info.store['servers'][server_name] = server_dict
            self.bot.info.save()

        event['from_to'].msg("I won't autojoin this channel after I'm kicked or shutdown. "
                             "The command to readd me is:  "
                             "{p}addchan".format(p=self.bot.settings.store['command_prefix']))
