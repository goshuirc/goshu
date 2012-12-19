#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
from gbot.libs.helper import html_unescape
import urllib.request, urllib.parse, urllib.error


class link(Module):
    name = 'link'

    def __init__(self):
        self.events = {
            'in' : {
                'pubmsg' : [(0, self.link)],
                'privmsg' : [(0, self.link)],
            },
        }

    def link(self, event):
        url_list = urls(unescape(event.arguments[0]))

        for url in url_list:
            if ('youtu' not in url) and ('nicovideo.jp/watch/sm' not in url):
                break  # only do this for youtube/niconico links
            if '/user/' in url:
                break  # don't do this for user pages, no useful info in title
            if 'youtuberepeat.com' in url:
                break  # don't do this for youtuberepeat.com, no title in there
            title = gettitle(url)
            if title == '':
                continue
            response = '*** title: ' + escape(html_unescape(title))
            self.bot.irc.msg(event, response, 'public')
            return  # don't spam us tryna return every title


def urls(input_str):
    url_list = []
    url_list += urls_protocol(input_str)
    url_list += urls_protocol(input_str, 'https')
    return url_list


def urls_protocol(input_str, protocol='http'):
    url_list = []
    while 1:
        if protocol+'://' in input_str:
            start_num = input_str.find(protocol+'://')
            input_str = input_str[start_num:]
            url_list.append(input_str.split()[0])
            if len(input_str.split(' ')) > 1:
                input_str = input_str.split(' ', 1)[1]
            else:
                break
        else:
            break

    return url_list


def gettitle(url):
    try:
        page = urllib.request.urlopen(url)
        old_title = page.read().decode('utf-8').split('<title>')[1].split('</title>')[0].strip()
        new_title = ''
        last_char_is_whitespace = False
        for title_char in old_title:
            if title_char.isspace():
                if last_char_is_whitespace:
                    continue
                else:
                    new_title += ' '
                    last_char_is_whitespace = True
            else:
                if last_char_is_whitespace:
                    last_char_is_whitespace = False
                new_title += title_char
        return new_title
    except:
        return ''
