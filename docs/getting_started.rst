Installing and Configuring Goshu
================================

Goshu makes it fairly easy to install, so long as you have a Unix-like environment. You can do the same thing on a Windows machine, but there will be more playing around to get packages and such working properly.


Prerequisites
-------------

* Git (to download the project itself)
* Python 3, with `Pip <http://pip.readthedocs.org/en/latest/installing.html>`_ installed


Installing
----------

First off, get a copy of Goshu using Git – this method makes it extremely easy to update and get new patches and fixes.

    $ git clone https://github.com/DanielOaks/goshu.git

Install Goshu's Python dependencies – this may take a while:

    $ pip3 install -r requirements.txt

And start the bot itself with:

    $ python3 goshu.py


Configuring
-----------

Once started as above, Goshu will ask you several questions including nicknames to use, master passwords, and IRC networks to connect to.

* Nick: This is the default nickname Goshu will use when connecting to IRC networks
* Password: This is the password users will enter to become a 'Bot Owner'
* Bot Command Prefix: This is what users will use to access Goshu's commands. For instance, ``.`` would require commands like ``.help``, ``'`` would require commands like ``'help``

.. WARNING::
    The Password above is EXTREMELY IMPORTANT. If a user can guess that, they can take control of your IRC bot and do anything they want with it.

    MAKE SURE THIS PASSWORD IS SECURE.


Account Setup
-------------

Once the bot connects to your given IRC networks, you'll need to make sure you can control the bot! You need to create a bot account, login, and make yourself a 'Bot Owner', and the below log shows how you can do that.

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

Once you've done this, you're right to go, Goshu is configured and ready to use! Simply invite her into whatever channel you want, and you can relax.

The next section will deal with day-to-day operations of the bot, and how to appoint Bot Admins to keep an eye on your bot when you can't.
