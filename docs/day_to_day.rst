Day-to-Day Operations
=====================

When running an IRC bot, it's useful to have administrative control over it. Things like module reloading, user privilege control, and even just being able to send messages and ``/me`` statements as your bot can be very useful tools.


Appointing 'Bot Admins'
-----------------------

Bot Admins are people who can access lots of the backend functions of Goshu. This includes loading / unloading / reloading modules, doing the same with the internal JSON stores, using the ``'me``, ``'msg``, and other sorts of commands.

To appoint a Bot Admin, you need to make sure the user has created their own account with your Goshu IRC bot. After this, you simply set their account level with the following:

    <dan> 'login coolguy57 usrpaswd
    <goshu> Login accepted!
    <dan> 'setaccess my_good_friend admin
    <goshu> Setting my_good_friend's access level to 5

This lets them do things with your Goshu bot if, for instance, it plays up and you're not online.
