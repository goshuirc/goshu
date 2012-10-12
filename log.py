#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import os
import sys

from gbot.libs.girclib import escape, unescape

if len(sys.argv) < 2:
    print('USAGE:')
    print('\t', sys.argv[0], '<logfile>')
    exit()

oldlog = open(sys.argv[1], 'r', encoding='utf8')
newlog = open(sys.argv[1]+'.new', 'w', encoding='utf8')

currentoldline = escape(oldlog.readline())
currentnewline = ''

while currentoldline != '':
    while len(currentoldline) > 0:
        try:
            if currentoldline[0] == '/':
                currentoldline = currentoldline[1:]
                
                if currentoldline[0] == '/':
                    currentnewline += '/'
                    currentoldline = currentoldline[1:]
                    
                elif currentoldline[0] == 'c':
                    currentoldline = currentoldline[1:]
                    if currentoldline[0].isdigit():
                        currentoldline = currentoldline[1:]
                        if currentoldline[0].isdigit():
                            currentoldline = currentoldline[1:]
                            if currentoldline[0] == ',':
                                currentoldline = currentoldline[1:]
                                if currentoldline[0].isdigit():
                                    currentoldline = currentoldline[1:]
                                    if currentoldline[0].isdigit():
                                        currentoldline = currentoldline[1:]
                    
                #elif currentoldline[0] in ['b', 'i', 'u', 'r']:
                #    currentoldline = currentoldline[1:]
                    
                else:
                    currentoldline = currentoldline[1:]
                    
            else:
                currentnewline += currentoldline[0]
                currentoldline = currentoldline[1:]
        except IndexError:
            ...
    
    newlog.write(currentnewline)
    currentoldline = escape(oldlog.readline())
    currentnewline = ''

oldlog.close()
newlog.close()

