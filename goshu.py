#!/usr/bin/env python
"""
goshu.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.bot import Bot
import json

bot = Bot()

try:
	settings_file = open('settings.json', 'r')
	settings = json.loads(settings_file.read())
	settings_file.close()
except:
	settings = None

settings = bot.irc.connection_prompt(settings)

try:
	settings_file = open('settings.json', 'w')
	settings_file.write(json.dumps(settings, sort_keys=True, indent=4))
	settings_file.close()
except:
	print 'Failed to save config file'

bot.irc.connect_dict(settings)

bot.irc.process_forever()
