#!/usr/bin/env python
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot    -    http://danneh.net/goshu

from time import strftime, localtime, gmtime
import random

from colorama import init
init() #colorama
from colorama import Fore, Back, Style

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape

class log_display(Module):
    name = "log_display"
    
    def __init__(self):
        self.events = {
            'all' : {
                'all' : [(-40, self.log)],
            }
        }
        self.nick_colors = {}
        random.seed()
    
    def log(self, event):
        if event.type == 'all_raw_messages':
            return
        
        #> 15:26:43
        output = '/c14'
        output += strftime("%H:%M:%S", localtime())
        
        #> -rizon-
        output += ' /c2-/c'
        output += event.server
        output += '/c2-/c '
        
        if event.type == '':
            ...
        
        elif event.type in ['welcome', 'yourhost', 'created', 'myinfo',
                            'featurelist', 'luserclient', 'luserop',
                            'luserchannels', 'luserme', 'n_local',
                            'n_global', 'luserconns', 'luserunknown',
                            'motdstart', 'motd', 'endofmotd', ]:
            for message in event.arguments:
                output += message + ' '
            
        elif event.type in ['privnotice', '439', ]:
            output += '/c14-'
            output += '/c13' + event.source.split('!')[0]
            try:
                output += '/c14('
                output += '/c13' + event.source.split('!')[1]
                output += '/c14)'
            except IndexError:
                output = output[:-1]
            output += '-/c '
            output += event.arguments[0]
        
        elif event.type in ['pubmsg', ]:
            output += '/c3-/c'
            output += event.target
            output += '/c3- '
            output += '/c14</c'
            try:
                if self.bot.irc.servers[event.server].info['channels'][event.target]['users'][event.source.split('!')[0]] == '': # prefix: +%@&~
                    output += ' '
                else:
                    output += self.bot.irc.servers[event.server].info['channels'][event.target]['users'][event.source.split('!')[0]]
            except:
                output += ' '
            output += self.nick_color(event.source.split('!')[0])
            output += '/c14>/c '
            output += event.arguments[0]
        
        elif event.type in ['privmsg', ]:
            output += '/c3-/c'
            if event.direction == 'in':
                output += event.source.split('!')[0]
            else:
                output += event.target
            output += '/c3- '
            output += '/c14</c'
            output += self.nick_color(event.source.split('!')[0])
            output += '/c14>/c '
            output += event.arguments[0]
        
        elif event.type in ['umode', ]:
            output += 'Mode change '
            output += '/c14[/c'
            output += event.arguments[0]
            output += '/c14]/c'
            output += ' for user '
            output += event.target
        
        elif event.type in ['mode', ]:
            output += '/c6-/c!/c6-/c '
            output += 'mode//'
            output += '/c10' + event.target + '/c '
            output += '/c14[/c'
            for arg in event.arguments:
                output += arg + ' '
            output = output[:-1] #strip last space
            output += '/c14]/c'
            output += ' by /b'
            output += event.source.split('!')[0]
            
        else:
            output += str(event.direction) + ' ' + str(event.type) + ' ' + str(event.source) + ' ' + str(event.target) + ' ' + str(event.arguments)
        
        #print(output)
        print(display_unescape(output + '/c'))
    
    def nick_color(self, nickhost):
        nick = nickhost.split('!')[0]
        if nick not in self.nick_colors:
            self.nick_colors[nick] = random.randint(2,13)
        return fore_colors[str(self.nick_colors[nick])] + nick

def display_unescape(input):
    output = ''
    while input != '':
        if input[0] == '/':
            if len(input) > 1 and input[1] == '/':
                input = input[2:]
                output += '/'
            elif len(input) > 1 and input[1] == 'c':
                fore = ''
                back = ''
                input = input[2:]
                in_fore = True
                
                while True:
                    if len(input) > 0 and input[0].isdigit():
                        digit = input[0]
                        input = input[1:]
                        
                        if in_fore:
                            if len(fore) < 2:
                                fore += digit
                            else:
                                input = digit + input
                                break
                        else:
                            if len(back) < 2:
                                back += digit
                            else:
                                input = digit + input
                                break
                    
                    elif len(input) > 0 and input[0] == ',':
                        if in_fore:
                            input = input[1:]
                            in_fore = False
                        else:
                            break
                    
                    else:
                        break
                
                if fore != '':
                    output += fore_colors[str(int(fore))]
                    if back != '':
                        output += back_colors[str(int(back))]
                
                else:
                    output += Fore.RESET
                    output += Back.RESET
            
            elif len(input) > 1 and input[1] in ['b', 'i', 'u', 'r']:
                input = input[2:]
            
        elif len(input) > 0:
            output += input[0]
            if len(input) > 0:
                input = input[1:]
        
        else:
            break
    
    return output
                

fore_colors = {
    '0' : Fore.WHITE+Style.BRIGHT,
    '1' : Fore.BLACK,
    '2' : Fore.BLUE,
    '3' : Fore.GREEN,
    '4' : Fore.RED+Style.BRIGHT,
    '5' : Fore.RED,
    '6' : Fore.MAGENTA,
    '7' : Fore.YELLOW,
    '8' : Fore.YELLOW+Style.BRIGHT,
    '9' : Fore.GREEN+Style.BRIGHT,
    '10' : Fore.CYAN,
    '11' : Fore.CYAN+Style.BRIGHT,
    '12' : Fore.BLUE+Style.BRIGHT,
    '13' : Fore.MAGENTA+Style.BRIGHT,
    '14' : Fore.BLACK+Style.BRIGHT,
    '15' : Fore.WHITE,
}
bold_fore_colors = {
    '0' : Fore.WHITE+Style.BRIGHT,
    '1' : Fore.BLACK+Style.BRIGHT,
    '2' : Fore.BLUE+Style.BRIGHT,
    '3' : Fore.GREEN+Style.BRIGHT,
    '4' : Fore.RED+Style.BRIGHT,
    '5' : Fore.RED+Style.BRIGHT,
    '6' : Fore.MAGENTA+Style.BRIGHT,
    '7' : Fore.YELLOW+Style.BRIGHT,
    '8' : Fore.YELLOW+Style.BRIGHT,
    '9' : Fore.GREEN+Style.BRIGHT,
    '10' : Fore.CYAN+Style.BRIGHT,
    '11' : Fore.CYAN+Style.BRIGHT,
    '12' : Fore.BLUE+Style.BRIGHT,
    '13' : Fore.MAGENTA+Style.BRIGHT,
    '14' : Fore.BLACK+Style.BRIGHT,
    '15' : Fore.WHITE+Style.BRIGHT,
}
back_colors = {
    '0' : '',
    '1' : '',
    '2' : '',
    '3' : '',
    '4' : '',
    '5' : '',
    '6' : '',
    '7' : '',
    '8' : '',
    '9' : '',
    '10' : '',
    '11' : '',
    '12' : '',
    '13' : '',
    '14' : '',
    '15' : '',
}