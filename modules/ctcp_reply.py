#!/usr/bin/env python
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot    -    http://danneh.net/goshu

from time import strftime, localtime, gmtime
from gbot.modules import Module
from gbot.libs.irclib3 import nm_to_n

class ctcp_reply(Module):
    name = "ctcp_reply"
    
    def __init__(self):
        self.events = {
            'in' : {
                'ctcp' : [(0, self.ctcp_reply)],
            },
        }
    
    def ctcp_reply(self, event):
        
        if event.arguments[0] == 'VERSION':
            self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source), 'VERSION Goshubot:3:None')
        
        elif event.arguments[0] == 'SOURCE':
            self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source), 'SOURCE github.com/Danneh/Goshubot')
        
        elif event.arguments[0] == 'USERINFO':
            userinfostring = None
            #userinfostring = "Please don't kline me, I'll play nice!"
            if userinfostring:
                self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source), "USERINFO :%s" % userinfostring)
        
        elif event.arguments[0] == 'CLIENTINFO':
            self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source), 'CLIENTINFO ') # to be continued
        
        elif event.arguments[0] == 'ERRMSG':
            #self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source, 'ERRMSG '+event.arguments()[1]+':ERRMSG echo, no error has occured') #could be bad, errmsg-storm, anyone?
            pass
        
        elif event.arguments[0] == 'TIME':
            self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source), 'TIME '+strftime("%a %b %d, %H:%M:%S %Y", localtime()))
        
        elif event.arguments[0] == 'PING':
            if len(event.arguments) > 1:
                self.bot.irc.servers[event.server].ctcp_reply(nm_to_n(event.source), "PING " + event.arguments[1])