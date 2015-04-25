#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from .users import USER_LEVEL_NOPRIVS, USER_LEVEL_ADMIN


class BaseCommand:
    """Provides for a generic command backend."""
    standard_command_privs = USER_LEVEL_NOPRIVS

    def __init__(self, base_info=None, **kwargs):
        # all general info
        if base_info:
            self.call = base_info[0]
            self.description = base_info[1]
            if len(base_info) > 2:
                self.call_level = base_info[2]
            else:
                self.call_level = self.standard_command_privs

            if len(base_info) > 3:
                self.view_level = base_info[3]
            else:
                self.view_level = self.call_level

        if kwargs:
            for key in kwargs:
                setattr(self, key, kwargs[key])

        if isinstance(self.description, str):
            self.description = [self.description]

        # defaults
        if not hasattr(self, 'alias'):
            self.alias = False


class AdminCommand(BaseCommand):
    standard_command_privs = USER_LEVEL_ADMIN


class Command(BaseCommand):
    """Actual module command."""
    def __init__(self, base_info=None, **kwargs):
        super().__init__(base_info, **kwargs)

        # defaults
        if not hasattr(self, 'user_whitelist'):
            self.user_whitelist = []
        if not hasattr(self, 'channel_whitelist'):
            self.channel_whitelist = []


class UserCommand:
    """Command from a client."""

    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments

    def arg_split(self, splits):
        """Split our arguments i number of times."""
        arg_list = []
        arg_cache = self.arguments

        for i in range(splits):
            new_arg, arg_cache = cmd_split(arg_cache)
            arg_list.append(new_arg)

        arg_list.append(arg_cache)

        return arg_list


# command splitting for modules
def cmd_split(in_str):
    if len(in_str.split()) > 1:
        do, args = in_str.split(' ', 1)
    else:
        do = in_str
        args = ''

    do = do.lower()

    return do, args


# standard commands
def acmd_ignore(self, event, command, usercommand):
    """Lets admins manage a list of 'ignored' targets
    
    @usage list
    @usage add <target>
    @usage del/rem <target>
    """
    do, args = usercommand.arg_split(1)

    if do == 'list':
        target_list = ' '.join(self.store.get('ignored', []))
        if not target_list:
            target_list = 'None'

        msg = 'Ignored targets: {}'.format(target_list)
        self.bot.irc.msg(event, msg, 'private')

    elif do == 'add':
        targets = args.lower().split()

        self.store.initialize_to('ignored', [])

        for target in targets:
            if target not in self.store.get('ignored'):
                self.store.append_to('ignored', target)

        msg = 'All given targets are now ignored'
        self.bot.irc.msg(event, msg, 'private')

    elif do in ('del', 'rem'):
        targets = args.lower().split()

        self.store.initialize_to('ignored', [])

        for target in targets:
            if target in self.store.get('ignored'):
                self.store.remove_from('ignored', target)

        msg = 'All given targets are no longer ignored'
        self.bot.irc.msg(event, msg, 'private')

standard_admin_commands = {
    'ignore': acmd_ignore,
}
