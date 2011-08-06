Goshubot
========
New Version: _goshu3_

Python3 IRC Bot, using the irclib3 and colorama libraries

Modules
-------
goshu3 is very modular, and allows you to simply drop goshu3 modules into the modules/ folder, where they're automatically loaded at runtime.  goshu3 comes with a number of default modules:
* Modules are represented like so: **dice**
* Commands are represented like so: _8ball_ 

**8ball**: adds _8ball_, returns basic 8ball answers
**danbooru**: adds _danbooru_ and _oreno_, for searching those sites
**dice**: adds _d_, parsing rpg dice like this: _d_ d6-3
**google**: adds _google_ and _youtube_, returns first result
**list**: adds _list_, lists current commands and help for commands

**ctcp_reply**: handles the basic CTCP requests - stuff like PING, VER, TIME
**info**: adds _info_, outputs testing info
**invite**: makes the bot autojoin any channel it's /invited to
**log_display**: prints/logs everything