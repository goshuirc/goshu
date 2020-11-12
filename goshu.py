#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import sys

import gbot

bot = gbot.Bot(config_path='config', modules_path='modules', debug=True, autostart='-y' in sys.argv[1:])

# start bot
bot.start()
