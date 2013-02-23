#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
"""extends several builtin functions and provides helper functions

The default Python library is extensive and well-stocked. There are some
times however, you wish a small task was taken care of for you. This module
if chock full of little extensions and helper functions I've written while
writing programs.
Things like converting bytes to a human-readable string, an easy progress
meter function---small interesting stuff like that.

Functions:

split_num() -- /lazy/ wrapper, to stop us bounds-checking when splitting
is_ok() -- prompt the user for yes/no and returns True/False
bytes_to_str() -- convert number of bytes to a human-readable format
filename_escape() -- escapes a filename (slashes removed, etc)
html_unescape() -- turns any html-escaped characters back to their normal equivalents
utf8_bom() -- removes the utf8 bom, because open() decides to leave it in

"""

import string


def split_num(line, chars=' ', maxsplits=1, empty=''):
    """/lazy/ wrapper, to stop us having to bounds-check when splitting

    Arguments:
    line -- line to split
    chars -- character(s) to split line on
    maxsplits -- how many split items are returned
    empty -- character to put in place of nothing

    Returns:
    line.split(chars, items); return value is padded until `maxsplits + 1`
    number of values are present

    """
    line = line.split(chars, maxsplits)
    while len(line) <= maxsplits:
        line.append(empty)

    return line


def is_ok(func, prompt, blank='', clearline=False):
    """Prompt the user for yes/no and returns True/False

    Arguments:
    prompt -- Prompt for the user
    blank -- If True, a blank response will return True, ditto for False,
             the default '' will not accept blank responses and ask until
             the user gives an appropriate response

    Returns:
    True if user accepts, False if user does not

    """
    while True:
        ok = func(prompt).lower().strip()

        try:
            if ok[0] == 'y' or ok[0] == 't' or ok[0] == '1':  # yes, true, 1
                return True
            elif ok[0] == 'n' or ok[0] == 'f' or ok[0] == '0':  # no, false, 0
                return False

        except IndexError:
            if blank == True:
                return True
            elif blank == False:
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

    if bytes >= (multiplexer ** 4):
        terabytes = float(bytes / (multiplexer ** 4))
        output = (precision_string % terabytes) + 'T'

    elif bytes >= (multiplexer ** 3):
        gigabytes = float(bytes / (multiplexer ** 3))
        output = (precision_string % gigabytes) + 'G'

    elif bytes >= (multiplexer ** 2):
        megabytes = float(bytes / (multiplexer ** 3))
        output = (precision_string % megabytes) + 'M'

    elif bytes >= (multiplexer ** 1):
        kilobytes = float(bytes / (multiplexer ** 1))
        output = (precision_string % kilobytes) + 'K'

    else:
        output = (precision_string % float(bytes)) + 'b'

    return output


def time_metric(secs=60):
    """Returns user-readable string representing given number of seconds."""
    time = ''
    for metric_secs, metric_char in [[60*60, 'h'], [60, 'm']]:
        if secs > metric_secs:
            time += '{}{}'.format(int(secs / metric_secs), metric_char)
            secs -= int(secs / metric_secs) * metric_secs
    if secs > 0:
        time += '{}s'.format(secs)
    return time


def metric(num):
    """Returns user-readable string representing given number."""
    for metric_raise, metric_char in [[9, 'B'], [6, 'M'], [3, 'k']]:
        if num > (10 ** metric_raise):
            return '{:.1f}{}'.format((num / (10 ** metric_raise)), metric_char)
    return str(num)


def filename_escape(unsafe, replace_char='_', valid_chars=string.ascii_letters+string.digits+'#._- '):
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


import xml.sax.saxutils as saxutils

_unescape_map = {
    '&#39;' : "'",
    '&#039;' : "'",
    '&quot;' : "'",
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
