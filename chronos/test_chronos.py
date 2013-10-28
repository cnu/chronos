#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import datetime

from api import parse


class EmptyTestCase(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual([], parse(''))

    def test_none(self):
        self.assertEqual([], parse(None))

    def test_nothing(self):
        self.assertEqual([], parse("no dates here"))


class ChristmasTestCase(unittest.TestCase):
    cur_year = datetime.date.today().year

    def test_christmas(self):
        out = [datetime.date(self.cur_year, 12, 25)]
        self.assertEqual(out, parse('this Christmas we'))

    def test_christmas_eve(self):
        out = [datetime.date(self.cur_year, 12, 24)]
        self.assertEqual(out, parse('this Christmas eve we'))


class NewYearTestCase(unittest.TestCase):
    cur_year = datetime.date.today().year
    next_year = cur_year + 1

    def test_new_year(self):
        out = [datetime.date(self.next_year, 1, 1)]
        self.assertEqual(out, parse("on new year we"))
        self.assertEqual(out, parse("on new years we"))
        self.assertEqual(out, parse("on new year's we"))
        self.assertEqual(out, parse("on newyear we"))
        self.assertEqual(out, parse("on newyears we"))

    def test_new_year_eve(self):
        out = [datetime.date(self.cur_year, 12, 31)]
        self.assertEqual(out, parse("on new year eve we"))
        self.assertEqual(out, parse("on new years eve we"))
        self.assertEqual(out, parse("on new year's eve we"))
        self.assertEqual(out, parse("on newyear eve we"))
        self.assertEqual(out, parse("on newyears eve we"))


if __name__ == '__main__': # pragma: no cover
    unittest.main()
