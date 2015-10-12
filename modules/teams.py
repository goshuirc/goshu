#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from girc.formatting import unescape

from gbot.modules import Module


class teams(Module):
    """Lets you create and interact with teams on your channel!"""

    def team_exists(self, server_name, channel_name, team_name):
        if self.store.has_key(['teams', server_name, channel_name, team_name]):
            return True
        else:
            return False

    def cmd_maketeam(self, event, command, usercommand):
        """Create a new team"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel, '
                                'by a channel operator')
            return

        if not event['target'].has_privs(event['source'], 'o'):
            event['source'].msg('Sorry, you need to be a channel operator to do this')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())
        team_name, description = usercommand.arg_split(lower=False)
        team_slug = team_name.casefold()

        print('TEAM NAME IS:', team_name)

        if self.store.has_key(['teams', server_name, channel_name, team_slug]):
            if description:
                self.store.set(['teams', server_name, channel_name, team_slug, 'name'], team_name)
                self.store.set(['teams', server_name, channel_name, team_slug, 'description'], description)
                event['target'].msg("Updated team's description")
        else:
            self.store.set(['teams', server_name, channel_name, team_slug, 'name'], team_name)
            self.store.set(['teams', server_name, channel_name, team_slug, 'description'], description)
            event['target'].msg('Created new team!')

    def cmd_deleteteam(self, event, command, usercommand):
        """Delete a team"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel, '
                                'by a channel operator')
            return

        if not event['target'].has_privs(event['source'], 'o'):
            event['source'].msg('Sorry, you need to be a channel operator to do this')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())
        team_name, description = usercommand.arg_split()
        team_name = team_name.casefold()

        if not self.team_exists(server_name, channel_name, team_name):
            event['target'].msg('That team does not exist')
            return

        self.store.remove(['teams', server_name, channel_name, team_name])
        event['target'].msg('Removed team')

    def cmd_teams(self, event, command, usercommand):
        """List all the teams"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())

        team_names = [i['name'] for i in self.store.get(['teams', server_name, channel_name], {}).values()]

        event['source'].msg('$bTeams:$r ' + ', '.join(sorted(team_names)))

    def cmd_jointeam(self, event, command, usercommand):
        """Join a team"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())
        team_name, description = usercommand.arg_split()
        team_name = team_name.casefold()

        if not self.team_exists(server_name, channel_name, team_name):
            event['target'].msg('That team does not exist')
            return

        team_nicks = self.store.get(['teams', server_name, channel_name, team_name, 'nicks'], [])
        team_userhosts = self.store.get(['teams', server_name, channel_name, team_name, 'userhosts'], [])

        nick = event['source'].nick.casefold()
        userhost = event['source'].userhost.casefold()

        joined = False

        if nick not in team_nicks:
            team_nicks.append(nick)
            self.store.set(['teams', server_name, channel_name, team_name, 'nicks'], team_nicks)
            joined = True
        if userhost not in team_userhosts:
            team_userhosts.append(userhost)
            self.store.set(['teams', server_name, channel_name, team_name, 'userhosts'], team_userhosts)
            joined = True

        if joined:
            event['target'].msg('Joined team {chan} / {team}'.format(chan=channel_name, team=team_name))
        else:
            event['source'].msg("You're already on that team")

    def cmd_leaveteam(self, event, command, usercommand):
        """Leave a team"""
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())
        team_name, description = usercommand.arg_split()
        team_name = team_name.casefold()

        if not self.team_exists(server_name, channel_name, team_name):
            event['target'].msg('That team does not exist')
            return

        team_nicks = self.store.get(['teams', server_name, channel_name, team_name, 'nicks'], [])
        team_userhosts = self.store.get(['teams', server_name, channel_name, team_name, 'userhosts'], [])

        nick = event['source'].nick.casefold()
        userhost = event['source'].userhost.casefold()

        left = False

        if nick in team_nicks:
            team_nicks.remove(nick)
            self.store.set(['teams', server_name, channel_name, team_name, 'nicks'], team_nicks)
            left = True
        if userhost in team_userhosts:
            team_userhosts.remove(userhost)
            self.store.set(['teams', server_name, channel_name, team_name, 'userhosts'], team_userhosts)
            left = True

        if left:
            event['target'].msg('Left team {chan} / {team}'.format(chan=channel_name, team=team_name))
        else:
            event['source'].msg("You're not on that team")

    def cmd_notifyteam(self, event, command, usercommand):
        """Notify all the members in a team about something

        @alias notify
        """
        if not event['target'].is_channel:
            event['source'].msg('Sorry, this command can only be used in a channel')
            return

        server_name = event['server'].name
        channel_name = unescape(event['target'].name.lower())
        team_name, description = usercommand.arg_split()
        team_name = team_name.casefold()

        if not self.team_exists(server_name, channel_name, team_name):
            event['target'].msg('That team does not exist')
            return

        team_nicks = self.store.get(['teams', server_name, channel_name, team_name, 'nicks'], [])
        team_userhosts = self.store.get(['teams', server_name, channel_name, team_name, 'userhosts'], [])

        nick = event['source'].nick.casefold()
        userhost = event['source'].userhost.casefold()

        if (event['target'].has_privs(event['source'], 'o') or
                nick in team_nicks or userhost in team_userhosts):
            nicks_to_notify = []

            for nick, user in event['target'].users.items():
                if (user.nick.casefold() in team_nicks or
                        user.userhost.casefold() in team_userhosts):
                    nicks_to_notify.append(user.nick)

            if nicks_to_notify:
                event['target'].msg('Notify: {team} : {nicks}'.format(**{
                    'team': self.store.get(['teams', server_name, channel_name, team_name, 'name']),
                    'nicks': ','.join(nicks_to_notify),
                }))

            else:
                event['target'].msg('No members of that team are currently online')
        else:
            event['source'].msg('You must be a member of this team or be a channel operator to do this')
