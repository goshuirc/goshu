#!/usr/bin/env python
"""
goshu.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.bot import Bot

bot = Bot()

#bot.irc.connect('127', '127.0.0.1', 6667, 'goshubot')
#bot.irc.privmsg('127', 'Danneh_', 'lolk')
connection = bot.irc.connection_prompt()
bot.irc.connect_dict(connection)

bot.irc.process_forever()
