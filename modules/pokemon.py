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
        'pokemon' : [self.get_pokemon, '--- get a random pokemon', 0],
        'poketeam' : [self.get_pokemon, '--- get a random pokemon team', 0],
        'pokerst' : [self.reset_pokemon, '--- reset corrupted pokemon save', 0],
      },
    }

    self.path = 'modules'+os.sep+'pokemon'+os.sep
    self.files = ['pokemon_list.json', 'corrupt_list.json']
    self.corrupted = None

    random.seed()

  def get_pokemon(self, event, command):
    team = []
    if command.command == 'pokemon' or self.corrupted:
      team.append(Monster(self.corrupted, self.path, self.files, True))
    else:
      while len(team) < 6:
        mon = Monster(self.corrupted, self.path, self.files, True)
        if mon.number != 0:
          team.append(mon)

    response = event.source.split('!')[0] + ' finds '
    if len(team) <= 1:
      response += 'a '

    for team_member in team:
      response += 'lvl ' + str(team_member.level) + ' ' + team_member.name + ', '# + ' (' + pad(str(team_member.number)) + '), '
    response = response[:-2]

    for team_member in team:
      if team_member.number == 0:
        self.corrupted = True

    self.bot.irc.servers[event.server].privmsg(event.from_to, response)

  def reset_pokemon(self, event, command):
    if not self.corrupted:
      return

    self.corrupted = None
    self.bot.irc.servers[event.server].action(event.from_to, 'takes out the cartridge, blows on it, and puts it back in')

class Monster:
  def __init__(self, corrupted=False, path='', files=['',''], generate=False):
    self.number = 0
    self.name = ''
    self.level = 0

    if generate:
      self.generate(corrupted, path, files)

  def generate(self, corrupted=False, path='', files=['','']):
    if corrupted:
      poke_list = json.loads(open(path+files[1]).read())
      self.number = random.randint(0, len(poke_list)-1)
      self.name = poke_list[self.number]
      self.level = str(random.randint(1, 100000))

    else:
      poke_list = json.loads(open(path+files[0]).read())
      self.number = random.randint(0, len(poke_list)-1)
      self.name = poke_list[self.number]
      self.level = str(random.randint(1, 100))

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
