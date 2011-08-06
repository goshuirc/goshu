Goshubot
========
New Version: _goshu3_

Python3 IRC Bot, using the [irclib3](http://github.com/Danneh/python-irclib) and [colorama](http://pypi.python.org/pypi/colorama) libraries

Modules
-------
goshu3 is very modular, and allows you to simply drop goshu3 modules into the modules/ folder, where they're automatically loaded at runtime. To disable any modules, simply delete them, or move them to a different folder (something like modules/disabled/ perhaps?)  
goshu3 comes with a number of modules to help you get started:

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

Events and IRC Libs
-------------------
Events and Event Handlers comprise most of goshu3's operation. girclib is a custom-written irclib3 wrapper, written to allow incoming _and_ outgoing events to be handled

If you want to see how girclib works, looking through source code should help quite a bit. Otherwise, I'm always happy to help at danneh@danneh.net

License
-------
Released under the Beer-Ware License; I don't drink, so soda instead of beer

```python
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a soda in return Daniel Oakley  
# ----------------------------------------------------------------------------
```