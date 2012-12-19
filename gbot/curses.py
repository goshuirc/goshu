#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import curses
import threading
import select
import math
import sys


class Curses:
    """Handles the goshu terminal display."""

    def __init__(self, bot):
        self.bot = bot

        # Setup curses everything
        self.stdscr = curses.initscr()

        curses.start_color()
        curses.use_default_colors()

        # Setup nice environment
        # curses.noecho()  # don't echo keys
        curses.cbreak()  # no enter-buffering
        self.stdscr.keypad(1)  # keypad input

        self.stdscr.clear()
        self.stdscr.border(0)

        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, -1)

        # Various windows
        self.wins = {}

        # Status bar, window info
        self.wins['info'] = curses.newwin(0, self.stdscr.getmaxyx()[1], 0, 0)
        self.wins['info'].idlok(0)
        self.wins['info'].clearok(1)
        self.wins['info'].scrollok(0)
        self.wins['info'].bkgdset(ord(' '), curses.color_pair(1) | curses.A_REVERSE)
        self.wins['info'].erase()
        self.wins['info'].noutrefresh()

        self.wins['info'].addstr(('Goshubot - connected to 40 zillion servers - eating 40,995 sudo sandwiches')[:self.stdscr.getmaxyx()[1]])

        # Messages
        self.pad = curses.newpad(self.stdscr.getmaxyx()[0]-3, self.stdscr.getmaxyx()[1])
        #  These loops fill the pad with letters; this is
        # explained in the next section
        for y in range(0, self.stdscr.getmaxyx()[0]-3):
            for x in range(0, self.stdscr.getmaxyx()[1]):
                try:
                    self.pad.addch(y, x, ord(' '))
                except curses.error:
                    pass

        # Displays current buffer, etc
        self.wins['buffer'] = curses.newwin(0, self.stdscr.getmaxyx()[1], self.stdscr.getmaxyx()[0]-2, 0)
        self.wins['buffer'].idlok(0)
        self.wins['buffer'].clearok(1)
        self.wins['buffer'].scrollok(0)
        self.wins['buffer'].bkgdset(ord(' '), curses.color_pair(1) | curses.A_REVERSE)
        self.wins['buffer'].erase()
        self.wins['buffer'].noutrefresh()

        self.wins['buffer'].addstr(('Goshubot - '*40)[:self.stdscr.getmaxyx()[1]])

        # Input bar
        self.wins['input'] = curses.newwin(0, self.stdscr.getmaxyx()[1], self.stdscr.getmaxyx()[0]-1, 0)
        self.wins['input'].idlok(0)
        self.wins['input'].clearok(1)
        self.wins['input'].scrollok(0)
        self.wins['input'].bkgdset(ord(' '), curses.color_pair(2))
        self.wins['input'].erase()
        self.wins['input'].noutrefresh()

        # Continue
        self.refresh()

    def start(self):
        CursesInput(self.bot).start()

    def shutdown(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    # Display functions
    def refresh(self):
        self.pad.refresh(0, 0,  1, 0,  self.stdscr.getmaxyx()[0]-3, self.stdscr.getmaxyx()[1])
        self.wins['info'].refresh()
        self.wins['buffer'].refresh()
        self.wins['input'].refresh()

    def pad_addline(self, line):
        num_lines = math.ceil(len(line)/self.stdscr.getmaxyx()[1])
        while num_lines > 0:
            num_lines -= 1

            self.pad.addstr(0, 0, 'Nope')  # Move cursor, delete old line
            self.pad.deleteln()

            if len(line) > self.stdscr.getmaxyx()[1]:
                show = line[:self.stdscr.getmaxyx()[1]-1]
                line = line[self.stdscr.getmaxyx()[1]-1:]
            else:
                show = line
            self.pad.addstr(self.stdscr.getmaxyx()[0] - 4, 0, show)  # Add new line

            self.refresh()

    # Input functions
    def get_input(self, prefix='>  ', password=False):
        self.wins['input'].erase()
        self.wins['input'].addstr(prefix)
        self.wins['input'].refresh()
        # Todo: if password, obscure chars
        line = self.wins['input'].getstr(0, len(prefix))
        return line.decode('utf-8')


class CursesInput(threading.Thread):

    def __init__(self, bot):
        threading.Thread.__init__(self, name='CursesInput')
        self.bot = bot
        self._stopp = threading.Event()

    # flag functions
    def stop(self):
        self._stopp.set()

    def stopped(self):
        return self._stopp.isSet()

    # Handling input
    def run(self):
        self.bot.curses.wins['input'].erase()
        self.bot.curses.wins['input'].refresh()

        buff = ''
        while True:
            select.select([sys.stdin], [], [])
            if self.stopped():
                return
            char = self.bot.curses.wins['input'].get_wch()
            if char is '\n':
                self.bot.curses.wins['input'].erase()
                self.bot.curses.wins['input'].refresh()
                self.bot.curses.pad_addline(buff)
                buff = ''
            else:
                buff += char
