#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from time import strftime, localtime
from gbot.modules import Module
from gbot.libs.girclib import NickMask


class ctcp_reply(Module):
    """Provides basic CTCP replies."""
    core = True

    def ctcp_listener(self, event):
        """Responds to CTCP messages

        @listen in ctcp highest
        """
        if event.arguments[0] == 'VERSION':
            message = 'VERSION Goshu:3:https://github.com/DanielOaks/goshu'

            # tell them owner nick(s) if one is online
            runner_level, online_runners = self.bot.accounts.online_bot_runners(event.server)
            if online_runners:
                trailing_s = 's' if len(online_runners) > 1 else ''
                runner_msg = "Hi, I'm an IRC bot! Online Contact{}:  {}".format(trailing_s, ' '.join(online_runners))
                self.bot.irc.msg(event, runner_msg, 'private')

            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, message)

        elif event.arguments[0] == 'USERINFO':
            userinfostring = None
            # userinfostring = "Please don't kline me, I'll play nice!"
            if userinfostring:
                self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'USERINFO :{}'.format(userinfostring))

        elif event.arguments[0] == 'CLIENTINFO':
            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'CLIENTINFO :Understood CTCP Pairs: CLIENTINFO, ERRMSG, PING, TIME, USERINFO, VERSION')

        elif event.arguments[0] == 'ERRMSG':
            # self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source, 'ERRMSG '+event.arguments()[1]+':ERRMSG echo, no error has occured') #could be bad, errmsg-storm, anyone?
            pass

        elif event.arguments[0] == 'TIME':
            self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'TIME {}'.format(strftime("%a %b %d, %H:%M:%S %Y", localtime())))

        elif event.arguments[0] == 'PING':
            if len(event.arguments) > 1:
                self.bot.irc.servers[event.server].ctcp_reply(NickMask(event.source).nick, 'PING ' + event.arguments[1])
