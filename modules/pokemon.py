#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from gbot.modules import Module
import random
import json
import os


class pokemon(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'commands': {
                'pokemon': [self.get_pokemon, '--- get a random pokemon'],
                'poketeam': [self.get_pokemon, '--- get a random pokemon team'],
                'pokerst': [self.reset_pokemon, '--- reset corrupted pokemon save'],
            },
        }

        self.path = 'modules'+os.sep+'pokemon'+os.sep
        self.files = ['pokemon_list.json', 'corrupt_list.json']
        self.corrupted = False

        random.seed()

    def get_pokemon(self, event, command, usercommand):
        team = []
        if usercommand.command == 'pokemon' or self.corrupted:
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
            response += 'lvl ' + str(team_member.level) + ' ' + team_member.name + ', '  # + ' (' + pad(str(team_member.number)) + '), '
        response = response[:-2]

        for team_member in team:
            if team_member.number == 0:
                self.corrupted = True

        self.bot.irc.msg(event, response, 'public')

    def reset_pokemon(self, event, command, usercommand):
        if not self.corrupted:
            return

        self.corrupted = None
        self.bot.irc.msg(event, 'takes out the cartridge, blows on it, and puts it back in', 'public')


class Monster:
    def __init__(self, corrupted=False, path='', files=['', ''], generate=False):
        self.number = 0
        self.name = ''
        self.level = 0

        if generate:
            self.generate(corrupted, path, files)

    def generate(self, corrupted=False, path='', files=['', '']):
        if corrupted:
            poke_list = json.loads(open(path + files[1]).read())
            self.number = random.randint(0, len(poke_list) - 1)
            self.name = poke_list[self.number]
            self.level = str(random.randint(1, 100000))

        else:
            poke_list = json.loads(open(path + files[0]).read())
            self.number = random.randint(0, len(poke_list) - 1)
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
