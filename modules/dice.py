#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import random

from gbot.modules import Module


class dice(Module):
    """Lets users roll rpg-like dics, such as d20, d6+3, etc."""

    def __init__(self, bot):
        Module.__init__(self, bot)

        random.seed()

    def cmd_dice(self, event, command, usercommand):
        """Rolls dice!

        @alias d
        @usage <dice>
        """
        try:
            iline = usercommand.arguments

            if iline == '':
                raise Exception

            if iline[0] == '-':
                iline = '0' + iline  # fixes negatives
            oline = []
            idice = []
            odice = []
            out_dice_line = ''

            # split line into seperate parts
            for split in iline.split('+'):
                oline = oline + split.split('-')

            for line in oline:
                if('d' in line):
                    if line.split('d')[0].isdigit():
                        if (len(str(line.split('d')[1])) > 6 or
                                len(str(line.split('d')[0])) > 10):
                            raise Exception
                        idice.append(line.split('d'))
                    else:
                        idice.append(['1', line.split('d')[1]])
                else:
                    idice.append(line.split('d'))

            # negatives
            i = 1
            for char in iline:
                if char == '+':
                    i += 1
                if char == '-':
                    if(len(idice[i]) == 2):
                        idice[i][1] = str(-int(idice[i][1]))
                    else:
                        idice[i][0] = str(-int(idice[i][0]))
                    i += 1

            # run and construct random numbers
            i = 0
            for split in idice:
                dice = []

                if(len(split) == 2):
                    for i in range(int(split[0])):
                        if(int(split[1]) > 0):
                            result = random.randint(1, int(split[1]))
                            dice.append(result)
                            out_dice_line += str(result) + ', '
                        else:
                            result = random.randint(int(split[1]), -1)
                            dice.append(result)
                            out_dice_line += str(result) + ', '
                        i += 1
                        if i > 10000:
                            raise Exception
                else:
                    dice += split

                odice.append(dice)

            # use calculated numbers to form result
            result = 0
            for li1 in odice:
                for li2 in li1:
                    result += int(li2)

            output = event['source'].nick + ': '
            output += iline + '    =    ' + str(result)
            if len(out_dice_line.split(',')) < 13:
                output += '    =    ' + out_dice_line[:-2]

            event['from_to'].msg(output)

        except:
            output_lines = ['DICE SYNTAX: {}d <dice>'.format(self.bot.settings.store['prefix']),
                            '        <dice> is a string like d12+4d8-13',
                            '        or any other permutation of rpg dice and numbers', ]

            for i in range(0, len(output_lines)):
                output = output_lines[i]

                event['source'].msg(output)
