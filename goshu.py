#!/usr/bin/env python3
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot    -    http://danneh.net/goshu

# fix for Windows' shitty default cp1252 encoding unicode output errors
import sys
if sys.stdout.encoding != 'utf-8':
    import warnings
    warnings.warn('unicode may be mangled due to non utf-8 stdout encoding: '+sys.stdout.encoding, UnicodeWarning)
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors='replace', line_buffering=True)

import gbot.bot
gbot.bot.DEBUG = True

print('Goshubot - IRC Bot')

bot = gbot.bot.Bot()


settings_path = 'settings.json'
bot.settings.use_file(settings_path, update=True)

info_path = 'info.json'
bot.info.use_file(info_path, update=True)

modules_path = 'modules'
bot.modules.load(modules_path)


bot.start()
print('\nfin~')