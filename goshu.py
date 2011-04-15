#!/usr/bin/env python3
"""
goshu.py - Goshubot
Copyright 2011 Daniel Oakley <danneh@danneh.net>

http://danneh.net/goshu/
"""

from gbot.bot import Bot
import json

print('Goshubot')

bot = Bot(prefix="'")

bot_settings_path = 'bot_settings.json'
server_settings_path = 'server_settings.json'

# bot settings
bot_settings = None
try:
	settings_file = open(bot_settings_path, 'r')
	bot_settings = json.loads(settings_file.read())
	settings_file.close()
except:
	bot_settings = None

bot_settings = bot.prompt_settings(bot_settings)

try:
	settings_file = open(bot_settings_path, 'w')
	settings_file.write(json.dumps(bot_settings, sort_keys=True, indent=4))
	settings_file.close()
except:
	print('Failed to save bot config file')

bot.process_settings(bot_settings)

# server settings
server_settings = None
try:
	settings_file = open(server_settings_path, 'r')
	server_settings = json.loads(settings_file.read())
	settings_file.close()
except:
	server_settings = None

server_settings = bot.irc.connection_prompt(server_settings)

try:
	settings_file = open(server_settings_path, 'w')
	settings_file.write(json.dumps(server_settings, sort_keys=True, indent=4))
	settings_file.close()
except:
	print('Failed to save server config file')

bot.irc.connect_dict(server_settings)

bot.irc.process_forever()
