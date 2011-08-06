Goshubot
========
New Version: _goshu3_

Python3 IRC Bot, using the [irclib3](http://github.com/Danneh/python-irclib) and [colorama](http://pypi.python.org/pypi/colorama) libraries

Modules
-------
goshu3 is very modular, and allows you to simply drop goshu3 modules into the modules/ folder, where they're automatically loaded at runtime. To disable any modules, simply delete them, or move them to a different folder (something like modules/disabled/ perhaps?). goshu3 already comes with a number of modules:

Modules are represented like so: **dice**  
Commands are represented like so: _8ball_ 

### User-oriented  (modify/remove these to your heart's content)
**8ball**: adds _8ball_, returns basic 8ball answers  
**danbooru**: adds _danbooru_ and _oreno_, for searching those sites  
**dice**: adds _d_, parsing rpg dice like this: _d_ d6-3  
**google**: adds _google_ and _youtube_, returns first search result  
**list**: adds _list_, lists current commands and help for commands

### Backend  (only modify/remove these if you know what you're doing)
**ctcp_reply**: handles the basic CTCP requests - stuff like PING, VER, TIME  
**info**: adds _info_, outputs testing info  
**invite**: makes the bot auto-join any channel it's /invited to  
**log_display**: prints/logs everything