#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module

class modules(Module):
    name = 'modules'

    def __init__(self):
        self.events = {
            'commands' : {
                'module' : [self.handle, ['<load//unload//reload> [name] --- load//unload//reload module specified by <name>', 'list --- list loaded modules'], 5],
            },
        }


    def handle(self, event, command):
        if not command.arguments:
            return

        do = command.arguments.split()[0]

        if do == 'list':
            self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], 'Loaded modules: ' + ', '.join(sorted(list(self.bot.modules.modules.keys()))))
            additional_modules = []
            for path in self.bot.modules.paths:
                modules = self.bot.modules.modules_from_path(path)
                for module in modules:
                    if module not in self.bot.modules.modules:
                        additional_modules.append(module)
            if len(additional_modules) > 0:
                self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], 'Additional avaliable modules: ' + ', '.join(sorted(additional_modules)))

        elif do in ['load', 'unload', 'reload']:
            if len(command.arguments.split()) < 2:
                return
            modules = command.arguments.split(' ', 1)[1].split()
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
                self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], action + 'ed: ' + ', '.join(sorted(succeed)))
            if fail:
                self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], action + ' Failed: ' + ', '.join(sorted(fail)))

