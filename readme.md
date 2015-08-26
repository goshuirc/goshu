![Goshu](docs/logo.png)

Goshu is a powerful IRC bot, written in Python3. Utilising simple YAML configuration files, a fast, extensible module system and useful, configurable logging, Goshu allows you to create your own personalised IRC bot in no time!

[Hosted Documentation](http://goshu.readthedocs.org/en/latest/)

girclib - Goshu IRC Library
---------------------------
The standard Python [irc](http://bitbucket.org/jaraco/irc) library, while great, lacks a number of fun and useful features including outgoing event trapping, user and channel info tracking, control codes / escaping, and ping timeout detection.

girclib is our internal irclib wrapper, written to extend and put a nice, useful interface on top of irclib's client module. It works similarly to irclib in terms of commands and operations, with extensions to handle tracking of users and channels, automatic NickServ identification, and automatic reconnection.

Unfortunately there isn't yet extensive documentation for girclib yet, but feel free to have a play with it – I'm always trying to extend the library and make it more useful!

Resources
---------
The Python libraries Goshu uses include [irc](http://bitbucket.org/jaraco/irc), [pyQuery](https://pypi.python.org/pypi/pyquery), [pyYAML](https://bitbucket.org/xi/pyyaml), [Requests](http://python-requests.org), [http_status](https://github.com/DanielOaks/http_status), [colorama](https://pypi.python.org/pypi/colorama), [pyparsing](http://pyparsing.wikispaces.com/), and [wolframalpha](https://pypi.python.org/pypi/wolframalpha)

[Miku image](https://www.flickr.com/photos/buddylindsey/4015238947/) in logo made by [Buddy Lindsey](https://www.flickr.com/photos/buddylindsey/), used under a CC BY 2.0 license.

License
-------
Released under the ISC License, specified in the LICENSE file.

Contact
-------
If you do something cool with my code, please feel free to [contact me](daniel@danieloaks.net)

For feature requests or contributions, feel free to make an issue or send a pull request!
