#!/usr/bin/env python2
# written by Daniel Oaks <daniel@danieloaks.net>
# IString Unit Tests

import os
import sys
import unittest

_base_dir = os.path.dirname(os.path.realpath(__file__))
_goshu_parent_dir = os.path.join(_base_dir, '..')
sys.path.append(_goshu_parent_dir)

from gbot.libs.girclib import IString


class IStringTestCase(unittest.TestCase):
    """Makes sure IStrings work properly."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equality_rfc(self):
        ist1 = IString('lol')
        ist1.set_std('rfc1459')

        self.assertEquals(ist1, 'LoL')  # normal str

        ist2 = IString('lOL')
        ist2.set_std('rfc1459')

        self.assertEquals(ist1, ist2)

        self.assertEquals(ist1.lower(), ist2.upper())

    def test_dict(self):
        ist1 = IString('lol')
        ist1.set_std('rfc1459')

        ist2 = IString('lOL')
        ist2.set_std('rfc1459')

        test_dict = {
            ist1: 'This is a test',
        }

        self.assertEquals(test_dict.get(ist2, None), 'This is a test')
