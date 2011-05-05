#!/usr/bin/env python3
"""
split_line_test.py - Goshubot test Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

import gbot.strings as strings

example = '/{indent:32,Fore:RED,Back:GREEN}lol al//righty then/{Style:RESET_ALL}okay?'
example_split = strings.split_line(example)
print('Split Line: %s' % example_split)