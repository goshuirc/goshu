#!/usr/bin/env python
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from time import strftime, localtime
from gbot.modules import Module
from gbot.libs.girclib import NickMask


class ctcp_reply(Module):

    def __init__(self, bot):
        Module.__init__(self, bot)
        self.events = {
            'in': {
                'ctcp': [(-30, self.ctcp_reply)],
            },
        }

    def ctcp_reply(self, event):

        if event.arguments[0] == 'VERSION':
            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'VERSION Goshubot:3:None')

        elif event.arguments[0] == 'SOURCE':
            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'SOURCE github.com/Danneh/Goshubot')

        elif event.arguments[0] == 'USERINFO':
            userinfostring = None
            # userinfostring = "Please don't kline me, I'll play nice!"
            if userinfostring:
                self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, "USERINFO :{}".format(userinfostring))

        elif event.arguments[0] == 'CLIENTINFO':
            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'CLIENTINFO :Understood CTCP Pairs: CLIENTINFO, ERRMSG, PING, SOURCE, TIME, USERINFO, VERSION')

        elif event.arguments[0] == 'ERRMSG':
            # self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source, 'ERRMSG '+event.arguments()[1]+':ERRMSG echo, no error has occured') #could be bad, errmsg-storm, anyone?
            pass

        elif event.arguments[0] == 'TIME':
            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'TIME {}'.format(strftime("%a %b %d, %H:%M:%S %Y", localtime())))

        elif event.arguments[0] == 'PING':
            if len(event.arguments) > 1:
                self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, "PING " + event.arguments[1])
