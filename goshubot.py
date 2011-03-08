#!/usr/bin/env python
"""
goshubot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import hashlib
import irclib
#irclib.DEBUG = True
from gbot.bot import Bot
import getpass

# connection info
network = '127.0.0.1'
port = 6667
channel = '#maid-rpg'
nick = 'goshuuuu' #Goshujin-Sama
name = 'goshu'
password = getpass.getpass('Enter bot password: ')

# irc object
irc = irclib.IRC()

# server object, connect and join channel
server = irc.server()
server.connect(network, port, nick, ircname=name)
server.join(channel)

# bot setup
bot = Bot(server, password, prefix='.', indent=3, module_path='modules')

# enable bot to respond
irc.add_global_handler('all_events', bot.handle)

# infinite loop
irc.process_forever()
