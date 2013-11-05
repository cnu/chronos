#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Text the basic chronos module"""

import unittest
import datetime

from .api import parse


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
    ref = datetime.datetime.utcfromtimestamp(25920000)

    def test_christmas(self):
        """Test for christmas date."""
        christmas = [datetime.date(self.cur_year, 12, 25)]
        self.assertEqual(christmas, parse('this Christmas we'))
        self.assertEqual(christmas, parse('this cHrIsTmAs we'))

    def test_christmas_eve(self):
        """Test for Christmas Eve date."""
        eve = [datetime.date(self.cur_year, 12, 24)]
        self.assertEqual(eve, parse('this Christmas eve we'))
        self.assertEqual(eve, parse('this ChristMas EvE we'))

    def test_ref(self):
        """Test for christmas & christmas eve date with ref date."""
        christmas = [datetime.date(self.ref.year, 12, 25)]
        eve = [datetime.date(self.ref.year, 12, 24)]
        self.assertEqual(christmas, parse('This christmas we', self.ref))
        self.assertEqual(eve, parse('this christmas eve we', self.ref))


class NewYearTestCase(unittest.TestCase):
    """Test for New year related dates."""
    cur_year = datetime.date.today().year
    ref = datetime.datetime.utcfromtimestamp(25920000)

    def test_new_year(self):
        """Test for New year dates."""
        next_year = self.cur_year + 1
        out = [datetime.date(next_year, 1, 1)]
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

    def test_ref(self):
        """Test for new year and new years eve with ref date."""
        newyear = [datetime.date(self.ref.year+1, 1, 1)]
        eve = [datetime.date(self.ref.year, 12, 31)]
        self.assertEqual(newyear, parse("On new Year we", self.ref))
        self.assertEqual(eve, parse("On new year eve we", self.ref))


class ISOTestCase(unittest.TestCase):
    """Test for dates formatted using the ISO 8601 format."""

    def test_basic(self):
        """Test for basic formats."""
        self.assertEqual([datetime.datetime(1990, 1, 1)], parse("In 1990-01-01 we"))
        self.assertEqual([datetime.datetime(1990, 1, 1, 10)], parse("In 1990-01-01T10 we"))
        self.assertEqual([datetime.datetime(1990, 1, 1, 10, 10)], parse("In 1990-01-01T10:10 we"))
        self.assertEqual([datetime.datetime(1990, 1, 1, 10, 10, 10)], parse("In 1990-01-01T10:10:10 we"))

        self.assertEqual([datetime.datetime(1990, 1, 1)], parse("In 1990-01-01 we"))
        self.assertEqual([datetime.datetime(1990, 1, 1, 10)], parse("In 1990-01-01t10 we"))
        self.assertEqual([datetime.datetime(1990, 1, 1, 10, 10)], parse("In 1990-01-01t10:10 we"))
        self.assertEqual([datetime.datetime(1990, 1, 1, 10, 10, 10)], parse("In 1990-01-01t10:10:10 we"))

    def test_multiple(self):
        """Test for basic formats."""
        text = """In 1990-01-01 and
                  1990-01-01T10 and
                  1990-01-01T10:10 and
                  1990-01-01T10:10:10
                  we"""
        output = [datetime.datetime(1990, 1, 1),
                  datetime.datetime(1990, 1, 1, 10),
                  datetime.datetime(1990, 1, 1, 10, 10),
                  datetime.datetime(1990, 1, 1, 10, 10, 10)]
        self.assertEqual(output, parse(text))


class WordDaysTestCase(unittest.TestCase):
    """Tests for relative days like today, tomorrow, yesterday, etc."""
    def test_days(self):
        """Test Today, tomorrow, yesterday, etc."""
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        yesterday = today - one_day
        tomorrow = today + one_day
        db_yesterday = yesterday - one_day
        da_tomorrow = tomorrow + one_day

        self.assertEqual([today], parse("foo today bar"))
        self.assertEqual([yesterday], parse("foo yesterday bar"))
        self.assertEqual([tomorrow], parse("foo tomorrow bar"))
        self.assertEqual([db_yesterday], parse("foo day before yesterday bar"))
        self.assertEqual([da_tomorrow], parse("foo day after tomorrow bar"))

        self.assertEqual([today], parse("foo Today bar"))
        self.assertEqual([yesterday], parse("foo Yesterday bar"))
        self.assertEqual([tomorrow], parse("foo Tomorrow bar"))
        self.assertEqual([db_yesterday], parse("foo Day Before Yesterday bar"))
        self.assertEqual([da_tomorrow], parse("foo Day After Tomorrow bar"))

        self.assertEqual([yesterday, today, tomorrow],
                         parse("foo yesterday, today and tomorrow bar"))

    def test_n_days(self):
        """Test N days ago, in N days, etc."""
        today = datetime.date.today()
        self.assertEqual([today - datetime.timedelta(days=3)], parse("foo 3 days back bar"))
        self.assertEqual([today - datetime.timedelta(days=10)], parse("foo 10 days ago bar"))
        self.assertEqual([today + datetime.timedelta(days=3)], parse("foo in 3 days bar"))
        self.assertEqual([today + datetime.timedelta(days=10)], parse("foo in 10 days bar"))

        self.assertEqual([today + datetime.timedelta(days=10),
                          today - datetime.timedelta(days=3)],
                         parse("foo in 10 days and 3 days back bar"))
        self.assertEqual([], parse("foo in 10 days ago bar"))

        self.assertEqual([], parse("foo in a while bar"))
        self.assertEqual([], parse("foo short while ago bar "))

        self.assertEqual([today + datetime.timedelta(days=1)], parse("foo in a day bar"))
        self.assertEqual([today - datetime.timedelta(days=1)], parse("foo a day ago bar"))
        self.assertEqual([today - datetime.timedelta(days=1)], parse("foo a day back bar"))
        self.assertEqual([], parse("foo next a day bar"))
        self.assertEqual([], parse("foo in a day ago bar"))
        self.assertEqual([], parse("foo in a day back bar"))

    def test_n_weeks(self):
        """Test N weeks ago, in N weeks, etc."""
        today = datetime.date.today()
        self.assertEqual([today - datetime.timedelta(weeks=3)], parse("foo 3 weeks back bar"))
        self.assertEqual([today - datetime.timedelta(weeks=10)], parse("foo 10 weeks ago bar"))
        self.assertEqual([today + datetime.timedelta(weeks=3)], parse("foo in 3 weeks bar"))
        self.assertEqual([today + datetime.timedelta(weeks=10)], parse("foo in 10 weeks bar"))

        self.assertEqual([today + datetime.timedelta(weeks=10),
                          today - datetime.timedelta(weeks=3)],
                         parse("foo in 10 weeks and 3 weeks back bar"))
        self.assertEqual([], parse("foo in 10 weeks ago bar"))

        self.assertEqual([], parse("foo in a while bar"))
        self.assertEqual([], parse("foo short while ago bar "))

        self.assertEqual([today + datetime.timedelta(weeks=1)], parse("foo in a week bar"))
        self.assertEqual([today - datetime.timedelta(weeks=1)], parse("foo a week ago bar"))
        self.assertEqual([today - datetime.timedelta(weeks=1)], parse("foo a week back bar"))
        self.assertEqual([], parse("foo next a week bar"))
        self.assertEqual([], parse("foo in a week ago bar"))
        self.assertEqual([], parse("foo in a week back bar"))

    def test_n_months(self):
        """Test N months ago, in N months, etc."""
        today = datetime.date.today()
        self.assertEqual([today - datetime.timedelta(days=3*30)], parse("foo 3 months back bar"))
        self.assertEqual([today - datetime.timedelta(days=10*30)], parse("foo 10 months ago bar"))
        self.assertEqual([today + datetime.timedelta(days=3*30)], parse("foo in 3 months bar"))
        self.assertEqual([today + datetime.timedelta(days=10*30)], parse("foo in 10 months bar"))

        self.assertEqual([today + datetime.timedelta(days=10*30),
                          today - datetime.timedelta(days=3*30)],
                         parse("foo in 10 months and 3 months back bar"))
        self.assertEqual([], parse("foo in 10 months ago bar"))

        self.assertEqual([], parse("foo in a while bar"))
        self.assertEqual([], parse("foo short while ago bar "))

        self.assertEqual([today + datetime.timedelta(days=1*30)], parse("foo in a month bar"))
        self.assertEqual([today - datetime.timedelta(days=1*30)], parse("foo a month ago bar"))
        self.assertEqual([today - datetime.timedelta(days=1*30)], parse("foo a month back bar"))
        self.assertEqual([], parse("foo next a month bar"))
        self.assertEqual([], parse("foo in a month ago bar"))
        self.assertEqual([], parse("foo in a month back bar"))

    def test_n_years(self):
        """Test N years ago, in N years, etc."""
        today = datetime.date.today()
        self.assertEqual([today - datetime.timedelta(days=3*365)], parse("foo 3 years back bar"))
        self.assertEqual([today - datetime.timedelta(days=10*365)], parse("foo 10 years ago bar"))
        self.assertEqual([today + datetime.timedelta(days=3*365)], parse("foo in 3 years bar"))
        self.assertEqual([today + datetime.timedelta(days=10*365)], parse("foo in 10 years bar"))

        self.assertEqual([today + datetime.timedelta(days=10*365),
                          today - datetime.timedelta(days=3*365)],
                         parse("foo in 10 years and 3 years back bar"))
        self.assertEqual([], parse("foo in 10 years ago bar"))

        self.assertEqual([], parse("foo in a while bar"))
        self.assertEqual([], parse("foo short while ago bar "))

        self.assertEqual([today + datetime.timedelta(days=1*365)], parse("foo in a year bar"))
        self.assertEqual([today - datetime.timedelta(days=1*365)], parse("foo a year ago bar"))
        self.assertEqual([today - datetime.timedelta(days=1*365)], parse("foo a year back bar"))
        self.assertEqual([], parse("foo next a year bar"))
        self.assertEqual([], parse("foo in a year ago bar"))
        self.assertEqual([], parse("foo in a year back bar"))

    def test_last_next(self):
        """Test last/next week/month/year combinations."""
        today = datetime.date.today()
        self.assertEqual([today - datetime.timedelta(weeks=1)], parse("foo last week bar"))
        self.assertEqual([today - datetime.timedelta(days=30)], parse("foo last month bar"))
        self.assertEqual([today - datetime.timedelta(days=365)], parse("foo last year bar"))

        self.assertEqual([today + datetime.timedelta(weeks=1)], parse("foo next week bar"))
        self.assertEqual([today + datetime.timedelta(days=30)], parse("foo next month bar"))
        self.assertEqual([today + datetime.timedelta(days=365)], parse("foo next year bar"))

        self.assertEqual([], parse("foo last weeks bar"))
        self.assertEqual([], parse("foo last months bar"))
        self.assertEqual([], parse("foo last years bar"))

        self.assertEqual([], parse("foo next weeks bar"))
        self.assertEqual([], parse("foo next months bar"))
        self.assertEqual([], parse("foo next years bar"))




if __name__ == '__main__': # pragma: no cover
    unittest.main()
