#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

from time import strftime, localtime

from gbot.modules import Module


class ctcp_reply(Module):
    """Provides basic CTCP replies."""
    core = True

    def ctcp_listener(self, event):
        """Responds to CTCP messages

        @listen in ctcp highest
        """
        if event['ctcp_verb'] == 'version':
            ver = 'Goshu:3:https://github.com/DanielOaks/goshu'

            # tell them owner nick(s) if one is online
            server_name = event['server'].name
            runner_level, online_runners = self.bot.accounts.online_bot_runners(server_name)
            if online_runners:
                trailing_s = 's' if len(online_runners) > 1 else ''
                runner_msg = ("Hi, I'm an IRC bot! Online Contact{}:  "
                              "{}".format(trailing_s, ' '.join(online_runners)))
                event['source'].msg(runner_msg)

            event['source'].ctcp_reply('VERISON', ver)

        elif event['ctcp_verb'] == 'userinfo':
            userinfostring = None
            # userinfostring = "Please don't kline me, I'll play nice!"
            if userinfostring:
                event['source'].ctcp_reply('USERINFO', userinfostring)

        elif event['ctcp_verb'] == 'clientinfo':
            understood = ['CLIENTINFO', 'ERRMSG', 'PING', 'TIME', 'USERINFO', 'VERSION']
            msg = 'Understood CTCP Pairs: {}'.format(','.join(understood))
            event['source'].ctcp_reply('CLIENTINFO', msg)

        elif event['ctcp_verb'] == 'errmsg':
            # event['source'].ctcp_reply(nm_to_n(event.source, 'ERRMSG '+event.arguments()[1]+':ERRMSG echo, no error has occured') #could be bad, errmsg-storm, anyone?
            pass

        elif event['ctcp_verb'] == 'time':
            event['source'].ctcp_reply('TIME', strftime('%a %b %d, %H:%M:%S %Y', localtime()))

        elif event['ctcp_verb'] == 'ping':
            event['source'].ctcp_reply('PING', event.ctcp_text)
