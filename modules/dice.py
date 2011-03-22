#!/usr/bin/env python
"""
dice.py - Goshubot dice Module
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.modules import Module
import random

class Dice(Module):
	
	name = "Dice"
	
	def __init__(self):
		self.events = {
			'commands' : {
				'd' : [self.dice, 'parse rpg dice strings', 0],
			},
		}
	
	def dice(self, iline, connection, event):
		server = self.bot.irc.server_nick(connection)
		channel = event.target().split('!')[0]
		nick = event.source().split('!')[0]
		
		if iline == '':
			output_lines = ['DICE SYNTAX: .d <dice>',
							'<dice> is a string like d12+4d8-13',
							'or any other permutation of rpg dice and numbers',]
			
			for i in range(0, len(output_lines)):
				if i > 0:
					output = ' ' * self.bot.indent
				else:
					output = ''
				
				output += output_lines[i]
				
				self.bot.irc.privmsg(server, nick, output)
			return
		
		try:
			if iline[0] == '-':
				iline = '0' + iline # fixes negatives
			oline = []
			idice = []
			odice = []
		
			# split line into seperate parts
			for split in iline.split('+'):
				oline = oline + split.split('-')
		
			for line in oline:
				if('d' in line):
					if line.split('d')[0].isdigit():
						idice.append(line.split('d'))
					else:
						idice.append(['1',line.split('d')[1]])
				else:
					idice.append(line.split('d'))
		
			# negatives
			i = 1
			for char in iline:
				if char == '+':
					i+= 1
				if char == '-':
					if(len(idice[i]) == 2):
						idice[i][1] = str(-int(idice[i][1]))
					else:
						idice[i][0] = str(-int(idice[i][0]))
					i += 1
		
			# run and construct random numbers
			for split in idice:
				dice = []
			
				if(len(split) == 2):
					for i in range(int(split[0])):
						if(int(split[1]) > 0):
							dice.append(random.randint(1, int(split[1])))
						else:
							dice.append(random.randint(int(split[1]), -1))
				else:
					dice += split
			
				odice.append(dice)
		
			# use calculated numbers to form result
			result = 0
			for li1 in odice:
				for li2 in li1:
					result += int(li2)
		
			output = event.source().split('!')[0]+': '+iline+' = '+str(result)
		
		except:
			output = event.source().split('!')[0]+': '+iline+' IS NOT A PROPER DICE STRING'
		
		connection.privmsg(event.target().split('!')[0], output)
