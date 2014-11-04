#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from . import gui, info, irc, modules, users
from .libs import log


class Bot:
    """Brings all of goshubot together in a nice happy class."""

    def __init__(self, debug=False):
        self.debug = debug
        self.logger = log.Logger

        self.accounts = users.AccountInfo(self)
        self.settings = info.BotSettings(self)
        self.info = info.IrcInfo(self)
        self.irc = irc.IRC(self)
        self.modules = modules.Modules(self)
        self.gui = gui.GuiManager(self)

    def start(self):
        self.irc.add_handler('all', 'all', self.modules.handle)
        self.irc.connect_info(self.info, self.settings)
        try:
            self.irc.process_forever()
        except KeyboardInterrupt:
            self.irc.disconnect_all('Goodbye')
