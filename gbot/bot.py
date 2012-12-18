#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from . import curses, info, irc, modules
import logging
import threading
import select
import sys


class Bot:
    """Brings all of goshubot together in a nice happy class."""

    def __init__(self, debug=False):
        self.debug = debug
        self.logger = logging.Logger

        self.accounts = info.Accounts(self)
        self.settings = info.Settings(self)
        self.info = info.Info(self)
        self.irc = irc.IRC(self)
        self.modules = modules.Modules(self)
        self.curses = curses.Curses(self)

    def start(self):
        self.irc.add_handler('all', 'all', self.modules.handle)
        self.irc.connect_info(self.info, self.settings)
        try:
            self.curses.start()
            self.irc.process_forever()
        except KeyboardInterrupt:
            self.irc.disconnect_all('Goodbye')

            for thread in threading.enumerate():
                if thread.getName() == 'CursesInput':
                    thread.stop()

        self.curses.pad_addline('Press Enter to exit')
        select.select([sys.stdin], [], [])
        self.curses.shutdown()
