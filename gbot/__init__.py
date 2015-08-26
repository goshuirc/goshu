#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import os

from colorama import init, Fore, Back, Style

from . import gui, info, irc, modules, users
from .libs import log

# section wrapping functions
# start colorama wrapping
init()


def _section_wrap(name):
    """Wrap the section name with appropriate colours, etc."""
    br = Fore.BLUE + Style.BRIGHT + '-*-' + Style.RESET_ALL
    return '\n\n{br} {name} {br}'.format(name=name, br=br)


def _subsection_wrap(name):
    """Wrap the subsection name with appropriate colours, etc."""
    br = Fore.BLUE + Style.BRIGHT + '-' + Style.RESET_ALL
    return '\n\n{br} {name} {br}'.format(name=name, br=br)


def _prompt_wrap(prompt):
    """Wrap the prompt with appropriate colours, etc."""
    br = Fore.MAGENTA + Style.BRIGHT + '*' + Style.RESET_ALL
    prompt = prompt.rstrip()
    return '{br} {prompt} '.format(prompt=prompt, br=br)


def _note_wrap(note):
    """Wrap the note with appropriate colours, etc."""
    br = Fore.YELLOW + Style.BRIGHT + '* NOTE:' + Style.RESET_ALL
    return '{br} {note}'.format(note=note, br=br)


def _success_wrap(name):
    """Return a little 'success' message."""
    check = Fore.GREEN + Style.BRIGHT + '✓' + Style.RESET_ALL
    return ' {check}  {name}'.format(name=name, check=check)


# Goshu
class Bot:
    """Brings all of goshubot together in a nice happy class."""
    def __init__(self, config_path='config', modules_path='modules', debug=False):
        self.debug = debug
        self.logger = log.Logger

        self._prompt_wraps = {
            'section': _section_wrap,
            'subsection': _subsection_wrap,
            'prompt': _prompt_wrap,
            'note': _note_wrap,
            'success': _success_wrap,
        }

        # load gui first, info components depend on it
        self.gui = gui.GuiManager(self)

        # initialize modules
        self.modules = modules.Modules(self, modules_path)
        self.modules.load_module_info()

        # config paths
        settings_path = os.path.join(config_path, 'bot.json')
        accountinto_path = os.path.join(config_path, 'info.json')
        info_path = os.path.join(config_path, 'irc.json')

        # info components
        self.settings = info.BotSettings(self, settings_path)
        self.accounts = users.AccountInfo(self, accountinto_path)
        self.info = info.IrcInfo(self, info_path)

        # other core components
        self.irc = irc.IRC(self)

        # setting up standard information
        if not self.settings.has_key('completed_initial_setup'):
            # manually centered, yay!
            print('\n'.join([
                '',
                "         Welcome to " + Fore.CYAN + Style.BRIGHT + "Goshu" + Style.RESET_ALL,
                " ~ " + Fore.MAGENTA + "The Hopefully-Stable IRC Bot" + Style.RESET_ALL + " ~ ",
                '',
                "It looks like this is the first time you've opened Goshu, so we're going "
                "to ask you some basic setup questions. You'll be setup in no time!",
            ]))
            self.settings.set('completed_initial_setup', True)

        self.settings.add_standard_keys()
        self.accounts.add_standard_keys()
        self.info.add_standard_keys()

        # load modules
        self.modules.load_init()


    def start(self):
        """Start IRC connections."""
        self.irc.add_handler('both', 'all', self.modules.handle)
        self.irc.connect_info(self.info, self.settings)
        self.irc.run_forever()
