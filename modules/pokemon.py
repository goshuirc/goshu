#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

from gbot.modules import Module
import random
import json
import os


class pokemon(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)

        self.path = os.path.join('modules', 'pokemon', '')  # '' to have trailing slash
        self.files = ['pokemon_list.json', 'corrupt_list.json']
        self.corrupted = False

        random.seed()

    def cmd_pokemon(self, event, command, usercommand):
        """Get a random pokemon

        @alias poketeam --- Get a Pokemon team
        """
        team = []
        if usercommand.command == 'pokemon' or self.corrupted:
            team.append(Monster(self.corrupted, self.path, self.files, True))
        else:
            while len(team) < 6:
                mon = Monster(self.corrupted, self.path, self.files, True)
                if mon.number != 0:
                    team.append(mon)

        response = event['source'].nick + ' finds '
        if len(team) <= 1:
            response += 'a '

        for team_member in team:
            response += 'lvl ' + str(team_member.level) + ' ' + team_member.name + ', '  # + ' (' + pad(str(team_member.number)) + '), '
        response = response[:-2]

        for team_member in team:
            if team_member.number == 0:
                self.corrupted = True

        event['from_to'].msg(response)

    def cmd_pokerst(self, event, command, usercommand):
        """Reset a corrupted pokemon save"""
        if not self.corrupted:
            return

        self.corrupted = None
        event['from_to'].me('takes out the cartridge, blows on it, and puts it back in')


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
