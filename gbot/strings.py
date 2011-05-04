#!/usr/bin/env python3
"""
strings.py - Goshubot strings Handler
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

from gbot.helper import splitnum

def retrieve_indent(string):
	""" Extracts indent from the beginning of the given string."""
	try:
		(indent_string, out_string) = splitnum(string, split_char='}')
		indent = int(indent_string[2:])
	except:
		indent = 0
		out_string = string
	return (indent, out_string)

def printable_len(in_string=None):
	""" Gives how many printable characters long the string is."""
	printable = 0
	if in_string:
		running = True
		while running:
			if in_string[0] == '/' and in_string[1] == '{':
				(temp_first, temp_last) = splitnum(in_string, split_char='}')
				in_string = temp_last
			elif in_string[0] == '/' and in_string[1] == '/':
				printable += 1
				in_string = in_string[2:]
			elif in_string[0].isprintable():
				printable += 1
				in_string = in_string[1:]
			if len(in_string) < 1:
				running = False
	return printable

def split_line(in_string=''):
	""" Splits line into an alternating string/list format, string for text and 
		list for attributes to be used/parsed."""
	return

def wrap(in_string, indent):
	try:
		rows, columns = os.popen('stty size', 'r').read().split()
	except: #not being executed in a terminal
		return in_string
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