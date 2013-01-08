#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

# fix for Windows' shitty default cp1252 encoding unicode output errors
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    import warnings
    warnings.warn('unicode may be mangled due to non utf-8 stdout encoding: '+sys.stdout.encoding, UnicodeWarning)
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors='replace', line_buffering=True)


import gbot

bot = gbot.Bot(debug=True)

accountinfo_path = 'config/info.json'
bot.accounts.use_file(accountinfo_path)

settings_path = 'config/bot.json'
bot.settings.use_file(settings_path, update=True)

info_path = 'config/irc.json'
bot.info.use_file(info_path, update=True)

modules_path = 'modules'
bot.modules.load_init(modules_path)

bot.start()
