#!/usr/bin/env python3
"""
log.py - Goshubot logging Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module
from gbot.helper import splitnum
import gbot.strings as strings
from time import strftime, localtime, gmtime
from colorama import init
init() #colorama
from colorama import Fore, Back, Style
import textwrap
import random
import os
import sys
import string

class Log:
	def __init__(self):
		self.Fore = {
			'BLACK' : '/{Fore.BLACK}',
			'RED' : '/{Fore.RED}',
			'GREEN' : '/{Fore.GREEN}',
			'YELLOW' : '/{Fore.YELLOW}',
			'BLUE' : '/{Fore.BLUE}',
			'MAGENTA' : '/{Fore.MAGENTA}',
			'CYAN' : '/{Fore.CYAN}',
			'WHITE' : '/{Fore.WHITE}',
			'RESET' : '/{Fore.RESET}',
		}
		self.Back = {
			'BLACK' : '/{Fore.BLACK}',
			'RED' : '/{Fore.RED}',
			'GREEN' : '/{Fore.GREEN}',
			'YELLOW' : '/{Fore.YELLOW}',
			'BLUE' : '/{Fore.BLUE}',
			'MAGENTA' : '/{Fore.MAGENTA}',
			'CYAN' : '/{Fore.CYAN}',
			'WHITE' : '/{Fore.WHITE}',
			'RESET' : '/{Fore.RESET}',
		}
		self.Style = {
			'DIM' : '/{Style.DIM}',
			'NORMAL' : '/{Style.NORMAL}',
			'BRIGHT' : '/{Style.BRIGHT}',
			'RESET_ALL' : '/{Style.RESET_ALL}',
		}
	
	def print_string(self, string, indent=None):
		""" Prints the given string."""
		if indent == None:
			(indent, string) = self.retrieve_indent(string)
		print(self.color_string_unescape(strings.wrap(string.strip(), indent)))
	
	def color_string_unescape(self, in_string=None):
		""" Replace color sequences with the proper codes and text for output."""
		if in_string:
			for code in self.Fore:
				in_string = in_string.replace(self.Fore[code], eval('Fore.'+code))
			for code in self.Back:
				in_string = in_string.replace(self.Back[code], eval('Back.'+code))
			for code in self.Style:
				in_string = in_string.replace(self.Style[code], eval('Style.'+code))
			in_string = in_string.replace('//', '/')
		else:
			in_string = ''
		return in_string

logger = Log()

#try:
path = sys.argv[1]
outfile = open(path, 'r')
for line in outfile:
	logger.print_string(line)
outfile.close()
#except:
#	print('cannot open file: %s' % sys.argv[1])
