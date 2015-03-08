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

# create bot
import gbot

bot = gbot.Bot(config_path='config', modules_path='modules', debug=True)

# start bot
bot.start()
