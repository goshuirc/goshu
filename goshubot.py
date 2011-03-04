#!/usr/bin/env python
"""
goshubot.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/maid/
"""

import irclib
irclib.DEBUG = True
from gbot.bot import Bot

# connection info
network = 'irc.rizon.net'
port = 6667
channel = '#maid-rpg'
nick = 'goshuuuu' #Goshujin-Sama
name = 'goshu'

# irc object
irc = irclib.IRC()

# server object, connect and join channel
server = irc.server()
server.connect(network, port, nick, ircname=name)
server.join(channel)

server.privmsg(channel, nick+', reporting for duty')

# modules
bot = Bot(prefix='.', indent=3)
bot.server = server
bot.load('modules')

# enable bot to respond
irc.add_global_handler('pubmsg', bot.handle)
irc.add_global_handler('privmsg', bot.handle)

# infinite loop
irc.process_forever()
