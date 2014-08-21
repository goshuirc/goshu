#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module


class modules(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands': {
                'module': [self.handle, ['<load/unload/reload> [name] --- load/unload/reload module specified by <name>', 'list --- list loaded modules'], 5],
            },
        }

    def handle(self, event, command, usercommand):
        if not usercommand.arguments:
            return

        do = usercommand.arguments.split()[0]

        if do == 'list':
            response = 'Loaded modules: ' + ', '.join(sorted(list(self.bot.modules.whole_modules.keys())))
            self.bot.irc.msg(event, response)
            additional_modules = []
            for path in self.bot.modules.paths:
                modules = self.bot.modules.modules_from_path(path)
                for module in modules:
                    if module not in self.bot.modules.whole_modules:
                        additional_modules.append(module)
            if len(additional_modules) > 0:
                response = 'Additional avaliable modules: ' + ', '.join(sorted(additional_modules))
                self.bot.irc.msg(event, response)

        elif do in ['load', 'unload', 'reload']:
            if len(usercommand.arguments.split()) < 2:
                return
            modules = usercommand.arguments.split(' ', 1)[1].split()
            succeed = []
            fail = []
            for module in modules:
                if do == 'load':
                    worked = self.bot.modules.load(module)
                elif do == 'unload':
                    worked = self.bot.modules.unload(module)
                else:  # reload
                    if self.bot.modules.unload(module):
                        worked = self.bot.modules.load(module)
                    else:
                        worked = False
                if worked:
                    succeed.append(module)
                else:
                    fail.append(module)
            action = do[0].upper() + do[1:]
            if succeed:
                self.bot.irc.msg(event, action + 'ed: ' + ', '.join(sorted(succeed)))
            if fail:
                self.bot.irc.msg(event, action + ' Failed: ' + ', '.join(sorted(fail)))
