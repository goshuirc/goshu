#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot	-	http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.girclib import escape
import random
import json
import os

class pokemon(Module):
	name = 'pokemon'
	
	def __init__(self):
		self.events = {
			'commands' : {
				'pokemon' : [self.pokemon, '--- get a random pokemon', 0],
				'pokerst' : [self.reset_pokemon, '--- reset corrupted pokemon save', 1],
			},
		}
		
		self.pokemon_path = 'modules'+os.sep+'pokemon'+os.sep
		self.pokemon_file = 'pokemon_list.json'
		self.corrupt_file = 'corrupt_list.json'
		self.corrupted = None
		
		random.seed()
	
	def pokemon(self, event, command):
		if self.corrupted:
			pokemon_list = json.loads(open(self.pokemon_path+self.corrupt_file).read())
			pokemon_num = random.randint(0, len(pokemon_list)-1)
			pokemon_level = str(random.randint(1, 100000))
		
		else:
			pokemon_list = json.loads(open(self.pokemon_path+self.pokemon_file).read())
			pokemon_num = random.randint(0, len(pokemon_list)-1)
			pokemon_level = str(random.randint(1, 100))
		
		#response = '*** pok' + b'\xc3\xa9'.decode() + 'mon: '
		response = event.source.split('!')[0]
		response += ' f/b/binds a lvl ' + pokemon_level + ' '
		response += pokemon_list[pokemon_num] + ' (' + pad(str(pokemon_num)) + ')'
		self.bot.irc.servers[event.server].privmsg(event.from_to, response)
		#>>> Nick finds a lvl72 MissingNO (000)
		if pokemon_num == 0:
			self.corrupted = True
	
	def reset_pokemon(self, event, command):
		if not self.corrupted:
			return
		
		self.corrupted = None
		self.bot.irc.servers[event.server].action(event.from_to, 'takes out the cartridge, blows on it, and puts it back in')

def pad(input, pad_num=3, pad_char='0'):
	output = ''
	for i in range(pad_num):
		if input == '':
			output = pad_char + output
		else:
			output += input[0]
			if len(input) > 1:
				input = input[1:]
			else:
				input = ''
	return output