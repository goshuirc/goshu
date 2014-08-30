Goshubot - _goshu3_
===================

Python3 IRC Bot, using the [irc](http://bitbucket.org/jaraco/irc) library

Installing/Configuring
----------------------
Install Python 3.x, install the dependencies below, and run goshu.py

Deps: [irc](http://bitbucket.org/jaraco/irc), [pyQuery](https://pypi.python.org/pypi/pyquery), [pyYAML](https://bitbucket.org/xi/pyyaml), [Requests](http://python-requests.org), [http_status](https://github.com/DanielOaks/http_status), colorama, pyparsing, wolframalpha

When you start the bot, it'll ask you several questions (including the master bot password!)

Once on IRC, privmsg the bot, create an account, and give yourself access as such:

```
<dan> 'register coolguy57 usrpaswd
<goshu> Account registered!
<dan> 'login coolguy57 usrpaswd
<goshu> Login accepted!

<dan> 'list
<goshu> *** Commands: calc, d, def, egg, google, help, list, loggedin, login, nickserv, pokemon, pokerst, poketeam, random, register, status, suggest, ud

<dan> 'owner botpassword
<goshu> You are now a bot owner

<dan> 'list
<goshu> *** Commands: calc, d, def, egg, google, help, info, join, list, loggedin, login, me, module, msg, nickserv, owner, part, pokemon, pokerst, poketeam, random, register, setaccess, status, suggest, ud
```

Modules
-------
goshu3 is very modular, and allows you to simply drop goshu3 modules into the modules/ folder, where they're automatically loaded at bot start.

To disable any modules, simply delete them, or move them to a different folder (something like modules/disabled/ perhaps?)

goshu3 comes with a number of modules to help you get started:

* Modules are represented like so: **dice**
* Commands are represented like so: _8ball_

### User-oriented  (modify/remove these to your heart's content)
* **dice**: adds _d_, parsing rpg dice like this: _d_ d6-3
* **dictionary**: adds _def_, definitions provided by wordnic (requires api key)
* **google**: adds _google_ and _youtube_, returns first search result _(also a dynamic command module)_
* **link**: posts the title of posted urls (restricted to youtube videos initially)
* **pokemon**: adds _pokemon_ and _pokedex_, returns random pokemon
* **random_module**: adds _random_
* **suggest**: adds _suggest_, allows users to make suggestions
* **urbandictionary**: adds _ud_, returns definition from urbandictionary

### Dynamic Command Modules (remove commands within these module's folders)
* **apiquery**: simple json query and replying
* **danbooru**: danbooru-based site search
* **google**: google search alias commands _(also provides user-oriented commands)_
* **responses**: various commands, simple random responses

### Backend  (only modify/remove these if you know what you're doing)
* **a_log_display**: prints/logs everything
* **accounts**: handles goshu's accounts
* **commands**: basic irc commands, things like _msg_, _me_, _join_
* **ctcp_reply**: handles the basic CTCP requests - stuff like PING, VER, TIME
* **info**: adds _info_, outputs testing info
* **invite**: makes the bot auto-join any channel it's /invited to
* **list**: adds _list_, lists current commands and help for commands

Dynamic Command Modules
-----------------------
Specific Dynamic Command Module keys and usage instructions

### ApiQuery Module
This module loads commands from the _modules/apiquery_ directory; That directory contains a multitude of files, each one providing a single command. The command-files are stored in json, and here are what the different keys do:
* **description**: sentence-long string describing the command
* **permission**: number representing the lowest permission level requirement required to access the command
* **url**: part of the url directly before the encoded user data
* **urlpost**: part of the url directly after the encoded user data
* **response**: series of lists, representing how the response is constructed from the given json
* **html_unescape**: whether to unescape stuff like &quot; and other html-escaped characters in json responses

### Danbooru Module
This module loads commands from the _modules/danbooru_ directory, keys:
* **description**: sentence-long string describing the command
* **permission**: number representing the lowest permission level requirement required to access the command
* **url**: base url of the danbooru installation
* **version**: if set to `"2"`, uses Danbooru v2 API

### Google Module
This module loads commands from the _modules/google_ directory, keys:
* **name**: name given to represent site
* **description**: sentence-long string describing the command
* **permission**: number representing the lowest permission level requirement required to access the command
* **url**: the url of the site to match, literally inserted after a "site:" google keyword

### Responses Module
This module loads commands from the _modules/responses_ directory, keys:
* **description**: sentence-long string describing the command
* **permission**: number representing the lowest permission level requirement required to access the command
* **initial**: string to process before getting randomised string
* **1**, **2**: list of strings to randomly pick from and process
* **1pre**, **1post**, **2pre**, **2post**: string to add to the beginning/end of every string in given list
* **1**: used when no argument is given
* **2**: used when argument is given

girclib
-------------------
irclib, while brilliant, lacks a number of features including: outgoing event trapping, info tracking, control codes, etc

I've written this girclib wrapper to address these. girclib works similarly to irclib in terms of commands and operations, but there are a few extensions to handle the above.

However, if you plan on using it for your own projects you may need some guidance

First off: Look at the source code. I know it may be obvious, but if you want to find out if you can do something, or how something's done, looking at either the girclib or gbot/irc.py source code will help quite a bit. If I haven't done it somewhere in there, chances are I haven't implemented it

<docs here>

License
-------
Released under the BSD 2-clause License

```
Copyright (c) 2014, Daniel Oaks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

Contact
-------
If you do something cool with my code, please feel free to [contact me](daniel@danieloaks.net)

For feature requests or contributions, feel free to make an issue, or send a pull request
