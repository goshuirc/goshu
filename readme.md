Goshubot - _goshu3_
===================

Python3 IRC Bot, using the [irclib3](http://github.com/Danneh/python-irclib) and [colorama](http://pypi.python.org/pypi/colorama) libraries

Installing/Configuring
----------------------
<section for users here, including installing python3, and installing the required libs>

Modules
-------
goshu3 is very modular, and allows you to simply drop goshu3 modules into the modules/ folder, where they're automatically loaded at runtime.
To disable any modules, simply delete them, or move them to a different folder (something like modules/disabled/ perhaps?)  
goshu3 comes with a number of modules to help you get started:

Modules are represented like so: **dice**  
Commands are represented like so: _8ball_ 

### User-oriented  (modify/remove these to your heart's content)
**danbooru**: adds _danbooru_ and _oreno_, for searching those sites  
**dice**: adds _d_, parsing rpg dice like this: _d_ d6-3  
**google**: adds _google_ and _youtube_, returns first search result  
**link**: posts the title of posted urls  
**list**: adds _list_, lists current commands and help for commands  
**pokemon**: adds _pokemon_ and _pokedex_, returns random pokemon  
**suggest**: adds _suggest_, allows users to make suggestions  

### Backend  (only modify/remove these if you know what you're doing)
**ctcp_reply**: handles the basic CTCP requests - stuff like PING, VER, TIME  
**info**: adds _info_, outputs testing info  
**invite**: makes the bot auto-join any channel it's /invited to  
**log_display**: prints/logs everything  
**responses**: dynamically loads commands from _modules/responses_  

### Responses Module
This module loads commands from the _modules/responses_ directory. That directory contains a multitude of files, each one providing a single command. The command-files are stored in json, and here are what the different keys do:  
**info**: sentence-long string describing the command  
**permission**: number representing the lowest permission level requirement required to access the command  
**initial**: string to process before getting randomised string  
**1**, **2**: list of strings to randomly pick from and process  
**1pre**, **1post**, **2pre**, **2post**: string to add to the beginning/end of every string in given list  
**1**: used when no argument is given  
**2**: used when argument is given  

girclib
-------------------
irclib, while brilliant, lacks a number of features including: outgoing event trapping, info tracking, etc

I've written this girclib wrapper to address these. girclib works similarly to irclib, in terms of commands and operations. However, if you plan on using it for your own projects you may need some guidance

First off: Look at the source code. I know it may be obvious, but if you want to find out if you can do something, or how something's done, looking at either the girclib or gbot/irc.py source code will help quite a bit. If I haven't done it somewhere in there, chances are I haven't implimented it

<docs here>

License
-------
Released under the Beer-Ware License

```python
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
```

Contact
-------
If you do something cool with my code, or you have feature requests, please feel free to contact me at danneh@danneh.net