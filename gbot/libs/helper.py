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

is_ok() -- prompt the user for yes/no and returns True/False
bytes_to_str() -- convert number of bytes to a human-readable format
filename_escape() -- escapes a filename (slashes removed, etc)
html_unescape() -- unescapes a string's &str; characters to normal
utf8_bom() -- removes the utf8 bom, because open() decides to leave it in

"""

import os
import sys
from getpass import getpass


def split_num(line, chars=' ', maxsplits=1):
    """.split(chars, maxsplit) wrapper, to mitigate 'more values to unpack'

    Arguments:
    line -- line to split
    chars -- character(s) to split line on
    maxsplits -- how many split items are returned

    Returns:
    line.split(chars, items); return value is padded until `maxsplits + 1`
    number of values are present

    """
    line = line.split(chars, maxsplits)
    while len(line) <= maxsplits:
        line.append('')

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


def print_progress_meter(percent, boxes=None, l_indent=1, r_indent=1, newline=False):
    """Prints a progress meter with the given percentage/options.

    Arguments:
    percent -- current percentage, from 0 to 100
    boxes -- if set, the progress meter will be `boxes` wide, otherwise it will
             expand to take up the terminal
    l_indent -- left indent
    r_indent -- right indent, making space for other info if needed
    newline -- whether to print a newline after the progress meter

    Details:
    print_progress_meter is meant to be used consecutively, and update the
    current progress meter line, rather than printing on a new line each
    iteration. Leaving `newline` as False will make it occur this way.

    """
    output = '\r'
    output += ' ' * l_indent
    output += '[ '

    if boxes == None:
        terminalinfo = terminal_info()
        boxes = terminalinfo['x']
        if boxes == None:  # could not find width
            boxes = 10
        boxes = boxes - len(output) - 2 - r_indent
    output += progress_meter(percent, boxes)
    output += ' ]'
    if newline:
        print(output)
    else:
        print(output, end='')


def progress_meter(percent, boxes=10):
    """Returns a progress meter for the given percent.

    Arguments:
    percent -- current percentage, from 0 to 100
    boxes -- meter will be `boxes` wide, empty boxes as spaces

    Returns:
    progress meter string, such as '######=     '

    """
    filledboxes = (percent / 100) * boxes
    (filledboxes, splitbox) = str(filledboxes).split('.')
    splitbox = float('0.'+splitbox)

    progressmeter = '#' * int(filledboxes)
    if splitbox == 0:
        progressmeter += ' ' * (boxes - int(filledboxes))
    elif splitbox < 0.5:
        progressmeter += '-'
        progressmeter += ' ' * (boxes - int(filledboxes) - 1)
    else:
        progressmeter += '='
        progressmeter += ' ' * (boxes - int(filledboxes) - 1)

    return progressmeter


def _fallback_terminal_info():
    x = None
    y = None

    return {
        'x' : x,
        'y' : y,
    }


def _win_terminal_info():
    from ctypes import windll, create_string_buffer
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

    if res:
        import struct

        (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy)\
        = struct.unpack("hhhhHhhhhhh", csbi.raw)

        x = right - left + 1
        y = bottom - top + 1

    else:
        x = None
        y = None

    return {
        'x' : x,
        'y' : y,
    }


def _unix_terminal_info():
    x = int(os.popen('tput cols', 'r').readline())
    y = int(os.popen('tput lines', 'r').readline())

    return {
        'x' : x,
        'y' : y,
    }

# bind terminal_info to correct os-specific function
try:
    import termios
    # it's possible there is an incompatible termios from the
    # McMillan Installer, make sure we have a UNIX-compatible termios
    termios.tcgetattr, termios.tcsetattr
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        terminal_info = _fallback_terminal_info
    else:
        terminal_info = _win_terminal_info
else:
    terminal_info = _unix_terminal_info

terminal_info.__doc__ = """Returns info about the current terminal, if working within one.

Returns:
Dictionary with the following keys/values:
    'x' -- width of terminal in number of characters
    'y' -- height of terminal in number of characters

Note:
value (of key/value pair) will be None if unable to get that specific info

"""


#def print(*args):
#    __builtins__.print(*args)
#    sys.stdout.flush()


import string


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
