#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

# Quite a lot of this module was taken, with permission, from https://github.com/electronicsrules/megahal
# In particular, the regexes and the display layout. Thanks a bunch, bro!

import re

from gbot.modules import Module
from gbot.libs.girclib import unescape
from gbot.libs.helper import get_url, json_format_extract

# import threading
# from watchdog.observers import Observer


# class JsonWatcher(threading.Thread):
#     def __init__(self, base, attr, folder, ext=None):
#         threading.Thread.__init__(self)
#         self.base= base
#         self.attr = attr
#         self.folder = folder
#         self.ext = ext

#     def run(self):
#         pass


class link(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'in' : {
                'pubmsg' : [(0, self.link)],
                'privmsg' : [(0, self.link)],
            },
        }
        # JsonWatcher(self, 'links', self.dynamic_folder, ext='.lnk').start()

    def link(self, event):
        url_list = self.urls(unescape(event.arguments[0]))

        for url in url_list:
            response = ''
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
                    url = unescape(provider['url'], unescape=complete_dict)
                    r = get_url(url)

                    if isinstance(r, str):
                        self.bot.irc.msg(event, '*** {}: {}'.format(provider['display_name'], r), 'public')
                        return

                    # parsing
                    if provider['format'] == 'json':
                        response += json_format_extract(provider, r.json())

            if response:
                self.bot.irc.msg(event, response, 'public')
            return  # don't spam us tryna return every title

    def urls(self, input_str):
        matches = re.search('(?:https?://)(\\S+)', input_str)
        # only returns a single URL. If we want multiple later, fix that
        if matches:
            return [matches[0]]
        else:
            return []

links = [
    {
        "display_name": "FimFiction",
        "match": "^(?:[^.]+\\.)?fimfiction\\.net\\/story\\/(\\d+)",
        "url": "http://fimfiction.net/api/story.php?story=@{regex_1}",
        "format": "json",
        "response": "@c2@b{title}@r by @c3@b{author}@r [@c6{rating};{status};{chapters}c;{words}w;{views}v@r] [@c6@b{time}@r] [@c3+{likes}@c4-{dislikes}@r] [{categories}]",
        "responses_dict": {
            'title': ["json", ["story", "title"]],
            'author': ["json", ["story", "author", "name"]],
            'rating': ["json", ["story", "content_rating_text"]],
            'status': ["json", ["story", "status"]],
            'chapters': ["json.num.metric", ["story", "chapter_count"]],
            'words': ["json.num.metric", ["story", "words"]],
            'views': ["json.num.metric", ["story", "views"]],
            'time': ["json.datetime.fromtimestamp", ["story", "date_modified"], "%H%MGMT %d%b%y"],
            'likes': ["json.num.metric", ["story", "likes"]],
            'dislikes': ["json.num.metric", ["story", "dislikes"]],
            'categories': ["json.dict.returntrue", ["story", "categories"], ";"]
        }
    },
    {
        "display_name": "You@5Tube@c",
        "match": "^(?:www\\.)?(?:(?:youtube\\.com/(?:watch)?(?:[?&]v=))|(?:youtu\\.be\\/))([a-zA-Z0-9-_]+)",
        "url": "http://gdata.youtube.com/feeds/api/videos/@{regex_1}?v=2&alt=jsonc",
        "format":"json",
        "response": "@c2@b{title}@r by @c3@b{author}@r [{length}] [{category}] [@c3+{likes}@r,@c4-{dislikes}@r,{comments}c,{views}v]",
        "responses_dict": {
            'title': ["json", ["data", "title"]],
            'author': ["json", ["data", "uploader"]],
            'length': ["json.seconds.metric", ["data", "duration"]],
            'category': ["json", ["data", "category"]],
            'likes': ["json.num.metric", ["data", "likeCount"]],
            'dislikes': ["yt.dislikes.metric", ["data", "ratingCount"], ["data", "likeCount"]],
            'comments': ["json.num.metric", ["data", "commentCount"]],
            'views': ["json.num.metric", ["data", "viewCount"]]
        }
    }
]
