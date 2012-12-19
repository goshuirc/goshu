#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import sys

from gbot.libs.girclib import escape, remove_control_codes

if len(sys.argv) < 2:
    print('USAGE:')
    print('\t', sys.argv[0], '<logfile>')
    exit()

oldlog = open(sys.argv[1], 'r', encoding='utf8')
newlog = open(sys.argv[1]+'.new', 'w', encoding='utf8')

line = escape(oldlog.readline())

while line != '':
    new_line = remove_control_codes(line)

    newlog.write(new_line)
    line = escape(oldlog.readline())
    new_line = ''

oldlog.close()
newlog.close()
