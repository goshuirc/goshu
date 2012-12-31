#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import curses, curses.ascii
import threading
import select
import math
import sys


class Curses:
    """Handles the goshu terminal display."""

    def __init__(self, bot):
        self.bot = bot
        self.wins = {}
        self.pad = None
        self.old_values = {}
        self.stdscr = None

        self.stdscr = curses.initscr()

        curses.start_color()
        curses.use_default_colors()
        self.stdscr.keypad(1)  # keypad input

        # Setup nice environment
        #curses.noecho()  # don't echo keys
        curses.cbreak()  # no enter-buffering

        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, -1)

        self.bot.irc.info_funcs.append(self.update_info)

        self.init_screen()

    def init_screen(self):
        # Various windows
        for win in ['info', 'buffer', 'input']:
            if win in self.wins:
                del self.wins[win]
        if self.pad:
            del self.pad

        self.stdscr.refresh()

        self.stdscr.clear()
        self.stdscr.border(0)

        # Status bar, window info
        self.wins['info'] = curses.newwin(0, self.stdscr.getmaxyx()[1], 0, 0)
        self.wins['info'].idlok(0)
        self.wins['info'].clearok(1)
        self.wins['info'].scrollok(0)
        self.wins['info'].bkgdset(ord(' '), curses.color_pair(1) | curses.A_REVERSE)
        self.wins['info'].erase()
        self.wins['info'].noutrefresh()

        if 'info' not in self.old_values:
            self.old_values['info'] = ''

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

        if 'pad' not in self.old_values:
            self.old_values['pad'] = []

        # Displays current buffer, etc
        self.wins['buffer'] = curses.newwin(0, self.stdscr.getmaxyx()[1], self.stdscr.getmaxyx()[0]-2, 0)
        self.wins['buffer'].idlok(0)
        self.wins['buffer'].clearok(1)
        self.wins['buffer'].scrollok(0)
        self.wins['buffer'].bkgdset(ord(' '), curses.color_pair(1) | curses.A_REVERSE)
        self.wins['buffer'].erase()
        self.wins['buffer'].noutrefresh()

        if 'buffer' not in self.old_values:
            self.old_values['buffer'] = ''

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
        self.win_addline('info', 'Goshubot - Loading')
        self.win_addline('buffer', 'Goshubot - '*40)
        CursesInput(self.bot).start()

    def shutdown(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    # Display functions
    def term_resize(self):
        self.init_screen()
        for win in ['info', 'buffer']:
            self.win_addline(win, self.old_values[win])
        for line in self.old_values['pad']:
            self.pad_addline(line, history=False)

    def refresh(self):
        self.wins['info'].refresh()
        self.wins['buffer'].refresh()
        self.wins['input'].refresh()
        self.pad.refresh(0, 0,  1, 0,  self.stdscr.getmaxyx()[0]-3, self.stdscr.getmaxyx()[1])

    def pad_addline(self, line, history=True):
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

        if history:
            self.old_values['pad'].append(line)
            while len(self.old_values['pad']) > 100:
                self.old_values['pad'] = self.old_values['pad'][1:]

    def win_addline(self, window, line):
        if len(line) < self.stdscr.getmaxyx()[1]:
            line += ' ' * (self.stdscr.getmaxyx()[1] - len(line))
        self.wins[window].addstr(0, 0, (line)[:self.stdscr.getmaxyx()[1]])
        self.old_values[window] = line

    # Input functions
    def get_input(self, prefix='', password=False):
        self.wins['input'].erase()
        self.wins['input'].addstr(prefix)
        self.wins['input'].refresh()
        # Todo: if password, obscure chars
        line = self.wins['input'].getstr(0, len(prefix))
        return line.decode('utf-8')

    # Update
    def update_info(self):
        line = 'Goshubot - '
        for server in self.bot.irc.servers:
            line += self.bot.irc.servers[server].info['name'] + ' - '
            line += str(len(self.bot.irc.servers[server].info['channels'])) + ' Channels, '
            line += str(len(self.bot.irc.servers[server].info['users'])) + ' Users ; '
        self.win_addline('info', line[:-3])

    # Buffer control
    def buffer_prev(self):
        """Go to the previous buffer."""
        self.pad_addline('Previous Buffer', history=False)

    def buffer_next(self):
        """Go to the next buffer."""
        self.pad_addline('Next Buffer', history=False)

    def buffer_cycle(self):
        """Cycle through the seperate buffers on the current merged buffer."""
        self.pad_addline('Cycle Buffer', history=False)


class CursesInput(threading.Thread):

    def __init__(self, bot):
        threading.Thread.__init__(self, name='CursesInput')
        self.bot = bot
        self._stopflag = threading.Event()

        self.specials = {
            '\x1b[A': self.input_up,     # up arrow
            '\x1b[B': self.input_down,   # down arrow
            '\x1b[C': self.input_left,   # left arrow
            '\x1b[D': self.input_right,  # right arrow
            '\x1b[1;3A': self.bot.curses.buffer_prev,  # alt + up arrow
            '\x1b[1;3B': self.bot.curses.buffer_next,  # alt + down arrow
            '\x1b[1;3C': self.bot.curses.buffer_prev,  # alt + left arrow
            '\x1b[1;3D': self.bot.curses.buffer_next,  # alt + right arrow
            '\x18': self.bot.curses.buffer_cycle,  # ctrl + x
        }

    # flag functions
    def stop(self):
        self._stopflag.set()

    def stopped(self):
        return self._stopflag.isSet()

    def handle_special(self, code):
        if code in self.specials:
            self.specials[code]()
        else:
            self.bot.curses.pad_addline('unknown key: ' + str([code]))

    # Handling input
    def run(self):
        self.bot.curses.wins['input'].erase()
        self.bot.curses.wins['input'].refresh()

        buff = ''
        special_buff = ''  # special characters, arrow keys, etc
        while True:
            select.select([sys.stdin], [], [])  # allows shutdown to work properly
            if self.stopped():
                return
            char = self.bot.curses.wins['input'].get_wch()

            # special chars
            if char == '\x1b':
                special_buff += char
            elif special_buff:
                special_buff += char
                if curses.ascii.isalpha(char):  # afaik, all specials end with an alpha char
                    self.handle_special(special_buff)
                    special_buff = ''

            elif char in self.specials:
                self.handle_special(char)

            # various curses keys, screen_resize, etc
            elif type(char) is int:
                continue

            # actual chars we care about
            elif char == '\n':
                self.bot.curses.wins['input'].erase()
                self.bot.curses.wins['input'].refresh()
                self.bot.curses.pad_addline(buff)
                if ':' in buff:
                    buff_list = []
                    for cha in buff.split(':')[1]:
                        buff_list.append(cha)
                    line = 'Characters are:  ' + buff.split(':')[0] + ' : ' + str(buff_list[1:])
                    self.bot.curses.pad_addline(line)
                    open('chars.txt', 'a', encoding='utf8').write(line + '\n')
                buff = ''
            else:
                buff += char

    # Input window control
    def input_up(self):
        """Up arrow, browse prev lines in the input list."""
        ...

    def input_down(self):
        """Down arrow, browse next lines in the input list."""
        ...

    def input_left(self):
        """Left arrow, previous character."""
        ...

    def input_right(self):
        """Right arrow, next character."""
        ...
