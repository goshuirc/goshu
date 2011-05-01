#!/usr/bin/env python3
"""
log.py - Goshubot logging Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.modules import Module
from gbot.helper import splitnum
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
		print(self.color_string_unescape(self.wrap(string.strip(), indent)))
	
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
	
	def wrap(self, in_string, indent):
		rows, columns = os.popen('stty size', 'r').read().split()
		output = ''
		running = True
		i = 1
		line = 0
		while running:
			char = in_string[0]
			
			if char == '/' and in_string[1] == '{':
				(temp_first, temp_last) = splitnum(in_string, split_char='}')
				output += temp_first+'}'
				in_string = temp_last
			elif char == '/' and in_string[1] == '/':
				output += '//'
				i += 1
				in_string = in_string[2:]
			elif char in string.printable:
				output += char
				i += 1
				in_string = in_string[1:]
			else:
				output += char
				in_string = in_string[1:]
			
			if int(i) > int(columns):
				output += ' '*int(indent)
				i = 1
				if line == 0:
					columns = int(columns) - int(indent)
				line += 1
			if len(in_string) < 1:
				running = False
		
		return output

logger = Log()

#try:
path = sys.argv[1]
outfile = open(path, 'r')
for line in outfile:
	logger.print_string(line)
outfile.close()
#except:
#	print('cannot open file: %s' % sys.argv[1])
