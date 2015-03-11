#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module


class list(Module):
    """Provides help and command listings to users."""
    core = True

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'in': {
                'privmsg': [(0, self.privmsg)]
            }
        }

    def privmsg(self, event):
        if event.arguments[0].lower() in ['help', 'hello', 'hi']:
            response = 'Hello! I am a bot, to view the avaliable commands, please type {prefix}list'.format(prefix=self.bot.settings.store['command_prefix'])
            self.bot.irc.msg(event, response)

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

                if self.bot.accounts.access_level(self.bot.accounts.account(event.source, event.server)) >= command.view_level:
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

            output.append('Note: to display information on a specific command, use @i{prefix}list <command>@i. eg: @i{prefix}list 8ball'.format(prefix=self.bot.settings.store['command_prefix']))

            for line in output:
                self.bot.irc.msg(event, line)
