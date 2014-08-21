#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

# fix for Windows' shitty default cp1252 encoding unicode output errors
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    import warnings
    warnings.warn('unicode may be mangled due to non utf-8 stdout encoding: ' + sys.stdout.encoding, UnicodeWarning)
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
