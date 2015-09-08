#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import gbot

bot = gbot.Bot(config_path='config', modules_path='modules', debug=True)

# start bot
bot.start()
