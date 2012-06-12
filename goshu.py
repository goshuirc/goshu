#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import os

# fix for Windows' shitty default cp1252 encoding unicode output errors
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    import warnings
    warnings.warn('unicode may be mangled due to non utf-8 stdout encoding: '+sys.stdout.encoding, UnicodeWarning)
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors='replace', line_buffering=True)

#delete old colorama install dir
if os.path.exists('autoinstall'):
    import shutil
    shutil.rmtree('autoinstall')
#automatically download/install colorama if needed
try:
    import colorama
except ImportError:
    download_url = 'http://pypi.python.org/packages/source/c/colorama/colorama-0.2.4.zip#md5=f1cf0b0bc675e0b9e22df28747ea1694'
    zip_path = 'autoinstall' + os.sep + 'colorama-0.2.4.zip'
    unzip_path = 'autoinstall' + os.sep + 'colorama-0.2.4'

    print('Colorama not found on system. Attempting to download from:')
    print(download_url)

    # download
    import urllib.request, urllib.parse, urllib.error

    if not os.path.exists('autoinstall'):
        os.makedirs('autoinstall')

    file = open(zip_path, 'wb')
    file.write(urllib.request.urlopen(download_url).read())
    file.close()

    # unzip
    import zipfile

    unzip = zipfile.ZipFile(zip_path)
    unzip.extractall('autoinstall')

    # and install
    old_path = os.getcwd()
    os.chdir(unzip_path)
    os.system(sys.executable + ' ' + 'setup.py build')
    os.system(sys.executable + ' ' + 'setup.py install')
    os.chdir(old_path)


import gbot.bot

print('Goshubot - IRC Bot')

bot = gbot.bot.Bot(debug=True)


accountinfo_path = 'config/info.json'
bot.accounts.use_file(accountinfo_path)

settings_path = 'config/bot.json'
bot.settings.use_file(settings_path, update=True)

info_path = 'config/irc.json'
bot.info.use_file(info_path, update=True)

modules_path = 'modules'
bot.modules.load(modules_path)


bot.start()
print('\nfin~')
