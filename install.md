Installing / Configuring
========================
First off, install Python3, since that's what Goshu runs on.

Get a copy of Goshu with the `git clone` command below:

    git clone https://github.com/DanielOaks/goshu.git

Install Goshu's Python dependencies with:

    pip3 install -r requirements.txt

And start the bot with:

    python goshu.py


When you start the bot, it'll ask you several questions including the master bot password and the servers it should connect to. Goshu is designed to handle anything from one single server to a few networks at once.

Once on IRC, message your bot, create an account, and give yourself full access as such:

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
