#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.users import USER_LEVEL_ADMIN
from gbot.modules import Module


class list(Module):
    """Provides help and command listings to users."""
    core = True

    def help_listener(self, event):
        """Watches for help messages

        @listen in privmsg
        """
        if event.arguments[0].lower() in ['help', 'hello', 'hi']:
            response = 'Hello! I am a bot, to view the avaliable commands, please type {prefix}list'.format(prefix=self.bot.settings.store.get('command_prefix'))

            # tell admins how to see acmds too
            if event.source_user_level > USER_LEVEL_ADMIN:
                response += ' and {prefix}list'.format(prefix=self.bot.settings.store.get('admin_command_prefix'))

            self.bot.irc.msg(event, response)

    def acmd_list(self, event, command, usercommand):
        """List all commands, or info on a given admin command

        @global
        @alias help
        """
        cmd_name, args = usercommand.arg_split(1)

        cmd_line_start = '    '
        cmd_line_limit = 256
        cmd_sep = ', '

        # getting help on a single acmd / module's acmds
        if cmd_name:
            self.bot.irc.msg(event, 'listing all acmds for module {}'.format(cmd_name))

        else:
            output = []

            # global admin commands
            output.append('*** Global Admin Commands: ')

            global_acmds = self.bot.modules.global_admin_commands
            for name, cmd in sorted(global_acmds.items()):
                # skip if this is just an alias for another global acmd
                any_true_commands = False
                for handle in cmd:
                    if not handle.alias:
                        any_true_commands = True
                if not any_true_commands:
                    continue

                # skip if user can't see the given global acmd
                can_see_acmd = False
                for handle in cmd:
                    if event.source_user_level >= handle.view_level:
                        can_see_acmd = True
                if not can_see_acmd:
                    continue

                # if output would be bigger than our limit, add new line
                if len(name) + len(cmd_sep) + len(output[-1]) > cmd_line_limit:
                    output.append(cmd_line_start)

                output[-1] += name + cmd_sep

            output[-1] = output[-1][:- len(cmd_sep)]  # remove last ', '

            # normal admin commands
            output.append('*** Admin Module Commands: ')

            modules = self.bot.modules.modules
            for name, mod in sorted(modules.items()):
                # make sure this module actually has acmd commands
                if not mod.admin_commands:
                    continue

                # if output would be bigger than our limit, add new line
                if len(name) + len(cmd_sep) + len(output[-1]) > cmd_line_limit:
                    output.append(cmd_line_start)

                output[-1] += name + cmd_sep

            output[-1] = output[-1][:- len(cmd_sep)]  # remove last ', '

            # write output
            output.append('Note: to display information on a specific command, use @i{prefix}list <command>@i. eg: @i{prefix}list help'.format(prefix=self.bot.settings.store.get('admin_command_prefix')))

            for line in output:
                self.bot.irc.msg(event, line)

    def cmd_list(self, event, command, usercommand):
        """List all commands, or info on given command

        @alias help
        """
        bot_commands = {}

        for module in sorted(self.bot.modules.modules):
            module_commands = self.bot.modules.modules[module].commands
            for name in sorted(module_commands):
                if name == '*':
                    continue
                command = module_commands[name]

                if event.source_user_level >= command.view_level:
                    bot_commands[name] = command

        if usercommand.arguments:
            # single command info
            name = usercommand.arguments.split()[0].lower()
            command_prefix = self.bot.settings.store['command_prefix']
            if name.startswith(command_prefix):
                name = name[len(command_prefix):]
            if name in bot_commands:
                command = bot_commands[name]

                # fix help display for single help strings
                for help_string in command.description:
                    response = '*** Command:  {prefix}{cmd} {desc}'.format(prefix=self.bot.settings.store['command_prefix'],
                                                                           cmd=name,
                                                                           desc=help_string)
                    self.bot.irc.msg(event, response)

        else:
            # list commands
            output = ['*** Commands: ']
            i = 0
            limit = 256
            for name in sorted(bot_commands.keys()):
                if bot_commands[name].alias:
                    continue
                if (len(output[i]) + len(name)) > limit:
                    output.append('    ')
                    i += 1
                output[i] += name + ', '
            output[i] = output[i][:-2]  # remove last ', '

            output.append('Note: to display information on a specific command, use @i{prefix}list <command>@i. eg: @i{prefix}list 8ball'.format(prefix=self.bot.settings.store.get('command_prefix')))

            for line in output:
                self.bot.irc.msg(event, line)
