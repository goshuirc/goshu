#!/usr/bin/env python
"""
helper.py - Goshubot Helper Commands
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

def splitnum(line, split_num=1, split_char=' '):
	temp_list_in = line.split(split_char)
	
	if split_num > 0:
		list_out = []
		
		for i in range(split_num):
			list_out.append(temp_list_in[0])
			del temp_list_in[0]
		
		string_out = ''
		for string in temp_list_in:
			string_out += string + ' '
		
		string_out = string_out[:-1] # remove last char
		
		list_out.append(string_out)
		
		return (list_out)
	
	else:
		return None
