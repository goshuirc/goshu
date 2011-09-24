#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
"""extends several builtin functions and provides helper functions

The default Python library is extensive and well-stocked. There are some
times however, you wish a small task was taken care of for you. This module
if chock full of little extensions and helper functions I've written while
writing programs.
Things like converting bytes to a human-readable string, an easy progress
meter function, small interesting stuff like that.

Functions:

is_ok() -- prompt the user for yes/no and returns True/False
bytes_to_str() -- convert number of bytes to a human-readable format
filename_escape() -- escapes a filename (slashes removed, etc)

"""

import os
import sys
from getpass import getpass

def split_num(line, chars=' ', maxsplits=1):
	""".split(chars, maxsplit) wrapper, to mitigate 'more values to unpack'
	
	Arguments:
	line -- line to split
	chars -- character(s) to split line on
	maxsplits -- how many split items are returned
	
	Returns:
	line.split(chars, items); return value is padded until `maxsplits + 1`
	number of values are present
	
	"""
	line = line.split(chars, maxsplits)
	while len(line) <= maxsplits:
		line.append('')
	
	return line

def is_ok(prompt, blank='', clearline=False):
	"""Prompt the user for yes/no and returns True/False
	
	Arguments:
	prompt -- Prompt for the user
	blank -- If True, a blank response will return True, ditto for False,
			 the default '' will not accept blank responses and ask until
			 the user gives an appropriate response
	
	Returns:
	True if user accepts, False if user does not
	
	"""
	while True:
		ok = new_input(prompt, newline=False, clearline=clearline).lower().strip()
		
		try:
			if ok[0] == 'y':
				return True
			elif ok[0] == 'n':
				return False
		
		except IndexError:
			if blank == True:
				return True
			elif blank == False:
				return False
		print('\r')


def bytes_to_str(bytes, base=2, precision=0):
	"""Convert number of bytes to a human-readable format
	
	Arguments:
	bytes -- number of bytes
	base -- base 2 'regular' multiplexer, or base 10 'storage' multiplexer
	precision -- number of decimal places to output
	
	Returns:
	Human-readable string such as '1.32M'
	
	"""
	if base == 2:
		multiplexer = 1024
	elif base == 10:
		multiplexer = 1000
	else:
		return None #raise error
	
	precision_string = '%.' + str(precision) + 'f'
	
	if bytes >= (multiplexer ** 4):
		terabytes = float(bytes / (multiplexer ** 4))
		output = (precision_string % terabytes) + 'T'
	
	elif bytes >= (multiplexer ** 3):
		gigabytes = float(bytes / (multiplexer ** 3))
		output = (precision_string % gigabytes) + 'G'
	
	elif bytes >= (multiplexer ** 2):
		megabytes = float(bytes / (multiplexer ** 3))
		output = (precision_string % megabytes) + 'M'
	
	elif bytes >= (multiplexer ** 1):
		kilobytes = float(bytes / (multiplexer ** 1))
		output = (precision_string % kilobytes) + 'K'
	
	else:
		output = (precision_string % float(bytes)) + 'b'
	
	return output


def print_progress_meter(percent, boxes=None, l_indent=1, r_indent=1, newline=False):
	"""Prints a progress meter with the given percentage/options.
	
	Arguments:
	percent -- current percentage, from 0 to 100
	boxes -- if set, the progress meter will be `boxes` wide, otherwise it will
			 expand to take up the terminal
	l_indent -- left indent
	r_indent -- right indent, making space for other info if needed
	newline -- whether to print a newline after the progress meter
	
	Details:
	print_progress_meter is meant to be used consecutively, and update the
	current progress meter line, rather than printing on a new line each
	iteration. Leaving `newline` as False will make it occur this way.
	
	"""
	output = '\r'
	output += ' ' * l_indent
	output += '[ '
	
	if boxes == None:
		terminalinfo = terminal_info()
		boxes = terminalinfo['x']
		if boxes == None: # could not find width
			boxes = 10
		boxes = boxes - len(output) - 2 - r_indent
	output += progress_meter(percent, boxes)
	output += ' ]'
	if newline:
		print(output)
	else:
		print(output, end='')

def progress_meter(percent, boxes=10):
	"""Returns a progress meter for the given percent.
	
	Arguments:
	percent -- current percentage, from 0 to 100
	boxes -- meter will be `boxes` wide, empty boxes as spaces
	
	Returns:
	progress meter string, such as '######=   '
	
	"""
	filledboxes = (percent / 100) * boxes
	(filledboxes, splitbox) = str(filledboxes).split('.')
	splitbox = float('0.'+splitbox)
	
	progressmeter = '#' * int(filledboxes)
	if splitbox == 0:
		progressmeter += ' ' * (boxes - int(filledboxes))
	elif splitbox < 0.5:
		progressmeter += '-'
		progressmeter += ' ' * (boxes - int(filledboxes) - 1)
	else:
		progressmeter += '='
		progressmeter += ' ' * (boxes - int(filledboxes) - 1)
	
	return progressmeter


def _fallback_terminal_info():
	x = None
	y = None
	
	return {
		'x' : x,
		'y' : y,
	}
	
def _win_terminal_info():
	from ctypes import windll, create_string_buffer
	h = windll.kernel32.GetStdHandle(-12)
	csbi = create_string_buffer(22)
	res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
	
	if res:
		import struct
		
		(bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy)\
		= struct.unpack("hhhhHhhhhhh", csbi.raw)
		
		x = right - left + 1
		y = bottom - top + 1
		
	else:
		x = None
		y = None
	
	return {
		'x' : x,
		'y' : y,
	}

def _unix_terminal_info():
	x = int(os.popen('tput cols', 'r').readline())
	y = int(os.popen('tput lines', 'r').readline())
	
	return {
		'x' : x,
		'y' : y,
	}

# bind terminal_info to correct os-specific function
try:
	import termios
	# it's possible there is an incompatible termios from the
	# McMillan Installer, make sure we have a UNIX-compatible termios
	termios.tcgetattr, termios.tcsetattr
except (ImportError, AttributeError):
	try:
		import msvcrt
	except ImportError:
		terminal_info = _fallback_terminal_info
	else:
		terminal_info = _win_terminal_info
else:
	terminal_info = _unix_terminal_info

terminal_info.__doc__ = """Returns info about the current terminal, if working within one.

Returns:
Dictionary with the following keys/values:
	'x' -- width of terminal in number of characters
	'y' -- height of terminal in number of characters

Note:
value (of key/value pair) will be None if unable to get that specific info

"""


def _fallback_new_input(prompt, password=False, newline=None, clearline=False):
	if password:
		return getpass(prompt)
	else:
		return input(prompt)

def _win_new_input(prompt, password=False, newline=True, clearline=False):
	if sys.stdin is not sys.__stdin__:
		return _fallback_new_input(prompt, newline, clearline)
	import msvcrt
	for c in prompt:
		msvcrt.putwch(c)
	
	if password:
		pw = ""
		
		while 1:
			c = msvcrt.getwch()
			if c == '\r' or c == '\n':
				break
			if c == '\003':
				raise KeyboardInterrupt
			if c == '\b':
				if len(pw) > 0:
					pw = pw[:-1]
			else:
				pw += c
		
		if clearline:
			for c in prompt:
				msvcrt.putwch('\b')
				msvcrt.putwch(' ')
				msvcrt.putwch('\b')
		
		if newline:
			msvcrt.putwch('\n')
		
		return pw
	
	else:
		pw = ""
		pwcursor = 0
		arrowkey = False
		
		while 1:
			c = msvcrt.getwch()
			if c == '\r' or c == '\n':
				break
			if c == '\003':
				raise KeyboardInterrupt
			if c == '\b':
				if len(pw) > 0 and pwcursor > 0:
					msvcrt.putwch('\b')
					msvcrt.putwch(' ')
					msvcrt.putwch('\b')
					pwcursor -= 1
					pw = pw[:pwcursor] + pw[pwcursor+1:]
					pw += ' '
					for ch in pw[pwcursor:]:
						msvcrt.putwch(' ')
					for ch in pw[pwcursor:]:
						msvcrt.putwch('\b')
					for ch in pw[pwcursor:]:
						msvcrt.putwch(ch)
					for ch in pw[pwcursor:]:
						msvcrt.putwch('\b')
					pw = pw[:-1]
			elif c.encode('utf-8') == b'\xc3\xa0':
				arrowkey = True
				continue
			elif arrowkey:
				if c == 'K': #leftarrow
					if pwcursor > 0:
						pwcursor -= 1
						msvcrt.putwch('\b')
					arrowkey = False
					continue
				elif c == 'M': #rightarrow
					if pwcursor < len(pw):
						pwcursor += 1
						msvcrt.putwch(pw[pwcursor-1])
					arrowkey = False
					continue
				elif c == 'G': #home
					while pwcursor > 0:
						pwcursor -= 1
						msvcrt.putwch('\b')
					arrowkey = False
					continue
				elif c == 'O': #end
					while pwcursor < len(pw):
						pwcursor += 1
						msvcrt.putwch(pw[pwcursor-1])
					arrowkey = False
					continue
				else:
					arrowkey = False
					continue
			else:
				pw = pw[:pwcursor] + c + pw[pwcursor:]
				for ch in pw[pwcursor:]:
					msvcrt.putwch(ch)
				for ch in pw[pwcursor+1:]:
					msvcrt.putwch('\b')
				pwcursor += 1
		
		if clearline:
			while pwcursor < len(pw):
				msvcrt.putwch(' ')
				pwcursor += 1
			for c in pw:
				msvcrt.putwch('\b')
				msvcrt.putwch(' ')
				msvcrt.putwch('\b')
			for c in prompt:
				msvcrt.putwch('\b')
				msvcrt.putwch(' ')
				msvcrt.putwch('\b')
		
		if newline:
			msvcrt.putwch('\n')
		
		return pw

# bind new_input to correct os-specific function
try:
	import termios
	# it's possible there is an incompatible termios from the
	# McMillan Installer, make sure we have a UNIX-compatible termios
	termios.tcgetattr, termios.tcsetattr
except (ImportError, AttributeError):
	try:
		import msvcrt
	except ImportError:
		new_input = _fallback_new_input
	else:
		new_input = _win_new_input
else:
	#new_input = _unix_new_input
	new_input = _fallback_new_input

if not terminal_info()['x']: #probably means we're running under an ide or similar
	new_input = _fallback_new_input

new_input.__doc__ = """Extends the input() builtin

Arguments:
prompt -- Prompt for the user
password -- If True, don't show characters
newline -- If True, print a newline after input
clearline -- If True, clear line after input, only works when newline is
			 True

Returns:
Input the user provides, same as the input() builtin

"""

def print(*args):
	__builtins__.print(*args)
	sys.stdout.flush()



import string
def filename_escape(unsafe, replace_char='_', valid_chars=string.ascii_letters+string.digits+'#._- '):
	"""Escapes a string to provide a safe local filename

Arguments:
unsafe -- Unsafe string to escape
replace_char -- Character to replace unsafe characters with
valid_chars -- Valid filename characters

Returns:
Safe local filename string

"""
	if not unsafe:
		return ''
	safe = ''
	for character in unsafe:
		if character in valid_chars:
			safe += character
		else:
			safe += replace_char
	return safe
