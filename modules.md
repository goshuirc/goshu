Modules
=======
Goshu is very modular, and allows you to simply drop modules into the modules/ folder, where they're automatically loaded at bot start or can be loaded at runtime by bot admins.

To disable any modules, simply disable them with the built-in module control command, delete them, or move them to a different folder.

Default Modules and Commands
----------------------------

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
* **a_log_display**: handles printing and logging of data
* **accounts**: handles Goshu's user accounts
* **commands**: basic irc commands, things like _msg_, _me_, _join_
* **ctcp_reply**: handles the basic CTCP requests - stuff like PING, VER, TIME
* **info**: adds _info_, outputs debugging information for developers
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
* **1**: response list used when no argument is given
* **2**: response list used when argument is given