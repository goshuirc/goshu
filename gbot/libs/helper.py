#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license
"""extends several builtin functions and provides helper functions

The default Python library is extensive and well-stocked. There are some
times however, you wish a small task was taken care of for you. This module
if chock full of little extensions and helper functions I've needed while
writing Goshu.

Small, interesting, self-contained functions that can probably be reused
elsewhere.
"""

import collections.abc
import datetime
import imp
import json
import os
import re
import string
import sys
import urllib.parse

from girc.formatting import escape
from http_status import Status
from pyquery import PyQuery as pq
import importlib
import requests
import xml.sax.saxutils as saxutils
import yaml


valid_filename_chars = string.ascii_letters + string.digits + '#._- '


def true_or_false(in_str):
    """Returns True/False if string represents it, else None."""
    in_str = in_str.lower()

    if in_str.startswith(('true', 'y', '1', 'on')):
        return True
    elif in_str.startswith(('false', 'n', '0', 'off')):
        return False
    else:
        return None


def split_num(line, chars=' ', maxsplits=1, empty=''):
    """/lazy/ wrapper, to stop us having to bounds-check when splitting.

    Arguments:
    line -- line to split
    chars -- character(s) to split line on
    maxsplits -- how many split items are returned
    empty -- character to put in place of nothing

    Returns:
    line.split(chars, items); return value is padded until `maxsplits + 1` number of values
    are present"""
    line = line.split(chars, maxsplits)
    while len(line) <= maxsplits:
        line.append(empty)

    return line


def is_ok(func, prompt, blank='', clearline=False):
    """Prompt the user for yes/no and returns True/False

    Arguments:
    prompt -- Prompt for the user
    blank -- If True, a blank response will return True, ditto for False, the default ''
             will not accept blank responses and ask until the user gives an appropriate
             response

    Returns:
    True if user accepts, False if user does not"""
    while True:
        ok = func(prompt).lower().strip()

        if len(ok) > 0:
            if ok[0] == 'y' or ok[0] == 't' or ok[0] == '1':  # yes, true, 1
                return True
            elif ok[0] == 'n' or ok[0] == 'f' or ok[0] == '0':  # no, false, 0
                return False

        else:
            if blank is True:
                return True
            elif blank is False:
                return False


def bytes_to_str(bytes, base=2, precision=0):
    """Convert number of bytes to a human-readable format

    Arguments:
    bytes -- number of bytes
    base -- base 2 'regular' multiplexer, or base 10 'storage' multiplexer
    precision -- number of decimal places to output

    Returns:
    Human-readable string such as '1.32M'

    """
    if base == 2:
        multiplexer = 1024
    elif base == 10:
        multiplexer = 1000
    else:
        return None  # raise error

    precision_string = '%.' + str(precision) + 'f'
    mebi_convert = True

    if bytes >= (multiplexer ** 4):
        terabytes = float(bytes / (multiplexer ** 4))
        output = (precision_string % terabytes) + 'T'

    elif bytes >= (multiplexer ** 3):
        gigabytes = float(bytes / (multiplexer ** 3))
        output = (precision_string % gigabytes) + 'G'

    elif bytes >= (multiplexer ** 2):
        megabytes = float(bytes / (multiplexer ** 2))
        output = (precision_string % megabytes) + 'M'

    elif bytes >= (multiplexer ** 1):
        kilobytes = float(bytes / (multiplexer ** 1))
        output = (precision_string % kilobytes) + 'K'

    else:
        output = (precision_string % float(bytes)) + 'B'
        mebi_convert = False

    # mebibytes and gibibytes all those weird HDD manufacturer terms
    if base == 10 and mebi_convert:
        num, base = output[:-1], output[-1]
        output = num + base.lower() + 'B'

    return output


def time_metric(secs=60, mins=0):
    """Returns user-readable string representing given number of seconds."""
    if mins:
        secs += (mins * 60)
    time = ''
    for metric_secs, metric_char in [[7 * 24 * 60 * 60, 'w'],
                                     [24 * 60 * 60, 'd'],
                                     [60 * 60, 'h'],
                                     [60, 'm']]:
        if secs > metric_secs:
            time += '{}{}'.format(int(secs / metric_secs), metric_char)
            secs -= int(secs / metric_secs) * metric_secs
    if secs > 0:
        time += '{}s'.format(secs)
    return time


def metric(num, metric_list=[[10 ** 9, 'B'], [10 ** 6, 'M'], [10 ** 3, 'k']], additive=False):
    """Returns user-readable string representing given value.

    Arguments:
    num is the base value we're converting.
    metric_list is the list of data we're working off.
    additive is whether we add the various values together, or separate them.

    Return:
    a string such as 345K or 23w6d2h53s"""
    output = ''
    for metric_count, metric_char in metric_list:
        if num > metric_count:
            if additive:
                format_str = '{}{}'
            else:
                format_str = '{:.1f}{}'

            num = (num / metric_count)
            if not additive:
                num = float(num)

            output += format_str.format(num, metric_char)

            if not additive:
                break

    # just in case no output
    if output == '':
        output = str(num)

    return output


def get_url(url, **kwargs):
    """Gets a url, handles all the icky requests stuff."""
    try:
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 20
        r = requests.get(url, **kwargs)
        r.status = Status(r.status_code)

        if not r.ok:
            return 'HTTP Error - {code} {name} - {description}'.format(**{
                'code': r.status.code,
                'name': r.status.name,
                'description': r.status.description
            })

    except requests.exceptions.Timeout:
        return 'Connection timed out'

    except requests.exceptions.RequestException as x:
        return '{}'.format(x.__class__.__name__)

    return r


def format_extract(format_json, input_element, format=None, debug=False, fail='Failure'):
    if not format:
        if 'format' in format_json:
            format = format_json['format']
        else:
            return 'No format for format_extract()'

    if 'debug' in format_json:
        debug = format_json['debug']

    # format-specific settings
    if format == 'json':
        input_element = json.loads(input_element)
        retrieve = json_return
    elif format == 'xml':
        # ignore xml namespaces
        input_element = input_element.replace(' xmlns:', ' xmlnamespace:')
        input_element = input_element.replace(' xmlns=', ' xmlnamespace=')
        retrieve = xml_return

    # format extraction - format kwargs
    format_dict = {}

    if 'response_dict' in format_json:
        for name in format_json['response_dict']:
            try:
                if isinstance(format_json['response_dict'][name], collections.abc.Callable):
                    try:
                        format_dict[name] = format_json['response_dict'][name](format_json,
                                                                               input_element)
                    except BaseException as x:
                        if debug:
                            return 'Unknown failure: {}'.format(x)
                        else:
                            return 'Code error'
                else:
                    format_dict[name] = retrieve(input_element,
                                                 format_json['response_dict'][name])

                if format_dict[name] is None:
                    return fail
            except KeyError:
                if debug:
                    return 'Fail on {}'.format(name)
                else:
                    return fail
            except IndexError:
                if debug:
                    return 'Fail on {}'.format(name)
                else:
                    return fail

    try:
        return format_json['response'].format(**format_dict)
    except KeyError:
        if debug:
            return 'Fail on format() key'
        else:
            return fail
    except IndexError:
        if debug:
            return 'Fail on format() index'
        else:
            return fail


def xml_return(input_xml, selector):
    pq_xml = pq(input_xml)

    if selector[0] == 'text':
        return selector[1]
    elif selector[0] == 'text.escape':
        return escape(selector[1])
    elif selector[0] == 'jquery':
        return pq_xml(selector[1]).text()
    elif selector[0] == 'jquery.attr':
        return pq_xml(selector[1]).attr(selector[2])


def json_return(input_json, selector):
    if selector[0] == 'text':
        return selector[1]
    elif selector[0] == 'text.escape':
        return escape(selector[1])
    elif selector[0] == 'json.lower':
        if len(selector) > 2:
            default = selector[2]
        else:
            default = ""
        return str(json_element(input_json, selector[1], default=default)).lower()
    elif selector[0] == 'json.quote_plus':
        if len(selector) > 2:
            default = selector[2]
        else:
            default = ""
        return urllib.parse.quote_plus(str(json_element(input_json, selector[1],
                                                        default=default)))
    elif selector[0] == 'json.num.metric':
        if len(selector) > 2:
            default = selector[2]
        else:
            default = 0
        return metric(int(json_element(input_json, selector[1], default=default)))
    elif selector[0] == 'json.datetime.fromtimestamp':
        if len(selector) > 2:
            default = selector[2]
        else:
            default = 0
        ts = json_element(input_json, selector[1], default=default)
        return datetime.datetime.fromtimestamp(ts).strftime(selector[2])
    elif selector[0] == 'json.dict.returntrue':
        keys = []
        json_dict = json_element(input_json, selector[1])
        for key in json_dict:
            if json_dict[key]:
                keys.append(key)
        return selector[2].join(keys)
    # before general json
    else:
        if len(selector) > 2:
            default = selector[2]
        else:
            default = None
        return escape(str(json_element(input_json, selector[1], default=default)))


def json_element(input_dict, query, default=None):
    """Runs through a data structure and returns the selected element."""
    for element in query:
        is_list_index = isinstance(element, int) and isinstance(input_dict, (list, tuple))
        if is_list_index or element in input_dict:
            input_dict = input_dict[element]
        else:
            return default
    return input_dict


def filename_escape(unsafe, replace_char='_', valid_chars=valid_filename_chars):
    """Escapes a string to provide a safe local filename

Arguments:
unsafe -- Unsafe string to escape
replace_char -- Character to replace unsafe characters with
valid_chars -- Valid filename characters

Returns:
Safe local filename string

"""
    if not unsafe:
        return ''
    safe = ''
    for character in unsafe:
        if character in valid_chars:
            safe += character
        else:
            safe += replace_char
    return safe

_unescape_map = {
    '&#39;': "'",
    '&#039;': "'",
    '&quot;': "'",
}


def html_unescape(input):
    """Turns any html-escaped characters back to their normal equivalents."""
    output = saxutils.unescape(input)
    for char in _unescape_map.keys():
        output = output.replace(char, _unescape_map[char])
    return output


def utf8_bom(input):
    """Strips BOM from a utf8 string, because open() leaves it in for some reason."""
    output = input.replace('\ufeff', '')
    return output


class JsonHandler:
    def __init__(self, base, folder, attr=None, callback_name=None, ext=None, yaml=False):
        if ext:
            self.pattern = [x.format(ext) for x in ['*.{}.yaml', '*.{}.json', '*_{}.py']]
        else:
            self.pattern = ['*.yaml', '*.json', '*.py']
        self.base = base
        self.attr = attr
        self.folder = folder
        self.ext = ext
        self.callback_name = callback_name
        self.yaml = yaml

        self.reload()

    def spread_new_json(self, new_json):
        if self.attr:
            setattr(self.base, self.attr, new_json)

        if self.callback_name:
            getattr(self.base, self.callback_name, None)(new_json)

    def reload(self):
        new_json = {}

        if not os.path.exists(self.folder):
            self.spread_new_json(new_json)
            return

        # loading
        folders_to_scan = [self.folder]

        # loading list of folders that contain modules
        for f in os.listdir(self.folder):
            if f == 'disabled':
                continue

            full_name = os.path.join(self.folder, f)
            if os.path.isdir(full_name):
                folders_to_scan.append(full_name)

        # loading actual modules
        for folder in folders_to_scan:
            for f in os.listdir(folder):
                full_name = os.path.join(folder, f)
                if os.path.isfile(full_name):
                    (extname, ext) = os.path.splitext(full_name)
                    if ext.lower() not in ['.json', '.yaml']:
                        continue

                    # check for loader-specific extension
                    if self.ext:
                        name, ext = os.path.splitext(extname)
                        pyfile = '{}_{}'.format('.'.join(name.split(os.sep)), self.ext)

                        # not really our module
                        if ext != os.extsep + self.ext:
                            continue
                    else:
                        name, ext = extname, ''
                        pyfile = '.'.join(name[2:].split(os.sep))

                    # NOTE: this is static, and that is bad
                    pyfile = pyfile.lstrip('..modules.')

                    # py file
                    if self.yaml:
                        try:
                            module = importlib.import_module(pyfile)
                            imp.reload(module)  # so reloading works
                        # we should capture this and output errors to stderr
                        except:
                            pass

                    # yaml / json
                    with open(full_name) as js_f:
                        if self.yaml:
                            try:
                                info = yaml.load(js_f.read())
                            # we should capture this and output errors to stderr
                            except Exception as ex:
                                print('failed to load YAML file', full_name, ':', ex)
                                continue
                        else:
                            info = json.loads(js_f.read())

                    # set module name and info
                    if 'name' not in info:
                        new_name = name.split('/')[-1]
                        info['name'] = [new_name]

                    new_json[info['name'][0]] = info

        # set info on base object and / or call callback
        self.spread_new_json(new_json)


# timedelta functions
_td_str_map = [
    ('d', 'days'),
    ('h', 'hours'),
    ('m', 'minutes'),
    ('s', 'seconds'),
]

_str_td = r''
for istr, td in _td_str_map:
    _str_td += r'\s*(?:(?P<' + td + r'>[0-9]+)\s*' + istr + r')?'

_TD_STR_REGEX = re.compile(_str_td)


def timedelta_to_string(delta):
    """Converts a timedelta dict to a string."""
    td_string = ''
    for istr, td in _td_str_map:
        if td in delta:
            td_string += str(delta[td])
            td_string += istr

    return td_string


def string_to_timedelta(td_string):
    """Converts a string to a timedelta dict."""
    match = _TD_STR_REGEX.match(td_string)
    delta = {}
    for istr, td in _td_str_map:
        if match.group(td):
            if '.' in match.group(td):
                val = float(match.group(td))
            else:
                val = int(match.group(td))
            delta[td] = val
    return delta


# path
def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
