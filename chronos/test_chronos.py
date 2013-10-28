#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Text the basic chronos module"""

import unittest
import datetime

from api import parse


class EmptyTestCase(unittest.TestCase):
    """Test for empty values passed - should return a empty list."""
    def test_empty_string(self):
        """Tests for a empty string."""
        self.assertEqual([], parse(''))

    def test_none(self):
        """Tests for None object."""
        self.assertEqual([], parse(None))

    def test_nothing(self):
        """Tests for a string which contains no dates at all."""
        self.assertEqual([], parse("nothing here"))


class ChristmasTestCase(unittest.TestCase):
    """Test christmas related dates."""
    cur_year = datetime.date.today().year

    def test_christmas(self):
        """Test for christmas date."""
        out = [datetime.date(self.cur_year, 12, 25)]
        self.assertEqual(out, parse('this Christmas we'))
        self.assertEqual(out, parse('this cHrIsTmAs we'))

    def test_christmas_eve(self):
        """Test for Christmas Eve date."""
        out = [datetime.date(self.cur_year, 12, 24)]
        self.assertEqual(out, parse('this Christmas eve we'))
        self.assertEqual(out, parse('this ChristMas EvE we'))


class NewYearTestCase(unittest.TestCase):
    """Test for New year related dates."""
    cur_year = datetime.date.today().year
    next_year = cur_year + 1

    def test_new_year(self):
        """Test for New year dates."""
        out = [datetime.date(self.next_year, 1, 1)]
        self.assertEqual(out, parse("on new year we"))
        self.assertEqual(out, parse("on New Year we"))
        self.assertEqual(out, parse("on new years we"))
        self.assertEqual(out, parse("on new year's we"))
        self.assertEqual(out, parse("on newyear we"))
        self.assertEqual(out, parse("on newyears we"))

    def test_new_year_eve(self):
        """Test for New Year eve dates."""
        out = [datetime.date(self.cur_year, 12, 31)]
        self.assertEqual(out, parse("on new year eve we"))
        self.assertEqual(out, parse("on New Year Eve we"))
        self.assertEqual(out, parse("on new years eve we"))
        self.assertEqual(out, parse("on new year's eve we"))
        self.assertEqual(out, parse("on newyear eve we"))
        self.assertEqual(out, parse("on newyears eve we"))


if __name__ == '__main__': # pragma: no cover
    unittest.main()
