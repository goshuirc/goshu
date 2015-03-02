Day-to-Day Operations
=====================

When running an IRC bot, it's useful to have administrative control over it. Things like module reloading, user privilege control, and even just being able to send messages and ``/me`` statements as your bot can be very useful tools.


Appointing 'Bot Admins'
-----------------------

Bot Admins are people who can access lots of the backend functions of Goshu. This includes loading / unloading / reloading modules, doing the same with the internal JSON stores, using the ``'me``, ``'msg``, and other sorts of commands.

To appoint a Bot Admin, you need to make sure the user has created their own account with your Goshu IRC bot. After this, you simply set their account level with the following:

::

    <dan> 'login coolguy57 usrpaswd
    <goshu> Login accepted!
    <dan> 'setaccess my_good_friend admin
    <goshu> Setting my_good_friend's access level to 5

This lets them do things with your Goshu bot if, for instance, it plays up and you're not online.

.. NOTE::
    Users are only able to give other users access levels up to and including their own. If you're an admin, the max level you can give another user is admin level, etc.

    In addition, only Admin and above are able to use the ``setaccess`` command.


Access Levels
-------------

Access levels go from 0 to 10, or:

::
    
    *(5)* Admin
    *(7)* Superadmin
    *(10)* Owner
