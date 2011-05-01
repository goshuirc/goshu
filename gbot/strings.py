#!/usr/bin/env python3
"""
strings.py - Goshubot strings Handler
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu
"""

def retrieve_indent(self, string):
	""" Extracts indent from the beginning of the given string."""
	try:
		(indent_string, out_string) = splitnum(string, split_char='}')
		indent = int(indent_string[2:])
	except:
		indent = 0
		out_string = string
	return (indent, out_string)
