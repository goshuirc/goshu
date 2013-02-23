#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

# Quite a lot of this module was taken from https://github.com/electronicsrules/megahal
# With permission, so thanks a bunch, bro!

import re
import requests
import datetime

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
from gbot.libs.helper import html_unescape, time_metric, metric


class link(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'in' : {
                'pubmsg' : [(0, self.link)],
                'privmsg' : [(0, self.link)],
            },
        }

    def link(self, event):
        url_list = urls(unescape(event.arguments[0]))

        for url in url_list:
            response = 'Failed'
            for provider in links:
                matches = re.match(provider['match'], url)
                if matches:
                    #response = '*** {}: '.format(provider['display_name'])
                    response = ''

                    match_index = 1
                    complete_dict = {}
                    for match in matches.groups():
                        if match != None:
                            complete_dict['regex_{}'.format(match_index)] = match
                            match_index += 1

                    match_dict = matches.groupdict()
                    for match in match_dict:
                        if match_dict[match] != None:
                            complete_dict['regex_{}'.format(match)] = match_dict[match]

                    # getting the actual file itself
                    try:
                        url = unescape(provider['url'], unescape=complete_dict)
                        r = requests.get(url, timeout=20)

                        if not r.ok:
                            response += 'HTTP Error - {code} {name}'.format(code=r.status.code, name=r.status.name)
                            self.bot.irc.msg(event, response, 'public')
                            return

                    except requests.exceptions.Timeout:
                        response += 'Connection timed out'
                        self.bot.irc.msg(event, response, 'public')
                        return

                    except requests.exceptions.RequestException as x:
                        response += '{}'.format(x.__class__.__name__)
                        self.bot.irc.msg(event, response, 'public')
                        return

                    # parsing
                    if provider['format'] == 'json':
                        response += json_data_exctact(r.json(), provider['response'])

            self.bot.irc.msg(event, response, 'public')
            return  # don't spam us tryna return every title

links = [
    {
        "display_name": "FimFiction",
        "match": "^(?:[^.]+\\.)?fimfiction\\.net\\/story\\/(\\d+)",
        "url": "http://fimfiction.net/api/story.php?story=@{regex_1}",
        "format": "json",
        "response": [
            ["text", "@c2@b"],
            ["json", ["story", "title"]],
            ["text", "@r by @c3@b"],
            ["json", ["story", "author", "name"]],
            ["text", "@r [@c6"],
            ["json", ["story", "content_rating_text"]],
            ["text", ";"],
            ["json", ["story", "status"]],
            ["text", ";"],
            ["json", ["story", "chapter_count"]],
            ["text", "c;"],
            ["json.num.metric", ["story", "words"]],
            ["text", "w;"],
            ["json.num.metric", ["story", "views"]],
            ["text", "v@r] [@c6@b"],
            ["json.datetime.fromtimestamp", ["story", "date_modified"], "%H%MGMT %d%b%y"],
            ["text", "@r] [@c3+"],
            ["json.num.metric", ["story", "likes"]],
            ["text", "@c4-"],
            ["json.num.metric", ["story", "dislikes"]],
            ["text", "@r] ["],
            ["json.dict.returntrue", ["story", "categories"], ";"],
            ["text", "]"]
        ]
    },
    {
        "display_name": "You@5Tube@c",
        "match": "^(?:www\\.)?(?:(?:youtube\\.com/(?:watch)?(?:[?&]v=))|(?:youtu\\.be\\/))([a-zA-Z0-9-_]+)",
        "url": "http://gdata.youtube.com/feeds/api/videos/@{regex_1}?v=2&alt=jsonc",
        "format":"json",
        "response": [
            ["text", "@c2@b"],
            ["json", ["data", "title"]],
            ["text", "@r by @c3@b"],
            ["json", ["data", "uploader"]],
            ["text", "@r ["],
            ["json.seconds.metric", ["data", "duration"]],
            ["text", "] ["],
            ["json", ["data", "category"]],
            ["text", "] [@c3+"],
            ["json.num.metric", ["data", "likeCount"]],
            ["text", "@r,@c4-"],
            ["yt.json.num.metric", ["data", "ratingCount"], ["data", "likeCount"]],
            ["text", "@r,"],
            ["json.num.metric", ["data", "commentCount"]],
            ["text", "c,"],
            ["json.num.metric", ["data", "viewCount"]],
            ["text", "v]"]
        ]
    }
]


def json_data_exctact(input_json, response_format):
    response = ''

    # try:
    for term in response_format:
        if term[0] == 'text':
            response += term[1]
        elif term[0] == 'text.escape':
            response += escape(term[1])
        elif term[0] == 'json.num.metric':
            response += metric(int(get_element(input_json, term[1])))
        elif term[0] == 'yt.json.num.metric':  # youtube
            response += metric(abs(int(get_element(input_json, term[1])) - int(get_element(input_json, term[2]))))
        elif term[0] == 'json.seconds.metric':
            response += time_metric(secs=get_element(input_json, term[1]))
        elif term[0] == 'json.datetime.fromtimestamp':
            response += datetime.datetime.fromtimestamp(get_element(input_json, term[1])).strftime(term[2])
        elif term[0] == 'json.dict.returntrue':
            keys = []
            json_dict = get_element(input_json, term[1])
            for key in json_dict:
                if json_dict[key]:
                    keys.append(key)
            response += term[2].join(keys)
        else:
            response += escape(str(get_element(input_json, term[1])))
    # except IndexError:
    #     return 'Nothing'
    # except KeyError:
    #     return 'Nothing'

    return response.replace('\n', ' ')


def get_element(input_dict, query):
    for element in query:
        input_dict = input_dict[element]
    return input_dict


def urls(input_str):
    url_list = []
    url_list += urls_protocol(input_str, 'http')
    url_list += urls_protocol(input_str, 'https')
    return url_list


def urls_protocol(input_str, protocol):
    url_list = []
    while 1:
        if protocol+'://' in input_str:
            start_num = input_str.find(protocol+'://')
            input_str = input_str[start_num:]
            url_list.append(input_str.split()[0][len(protocol+'://'):])
            if len(input_str.split(' ')) > 1:
                input_str = input_str.split(' ', 1)[1]
            else:
                break
        else:
            break

    return url_list


def gettitle(url):
    try:
        r = requests.get(url, timeout=20)

        if not r.ok:
            return 'HTTP Error - {code} {name}'.format(code=r.status_code, desc=r.status_name)

    except requests.exceptions.Timeout:
        return 'Connection timed out'

    except requests.exceptions.RequestException as x:
        return '{}'.format(x.__class__.__name__)

    old_title = r.text.split('<title>')[1].split('</title>')[0].strip()
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
