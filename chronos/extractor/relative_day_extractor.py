#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract date & time from text having today, tomorrow, yesterday, etc."""

import re
import datetime

from chronos.extractor.base import Extractor


class RelativeDayExtractor(Extractor):
    def __init__(self, ref=None):
        super(RelativeDayExtractor, self).__init__(ref)
        self.patterns = {re.compile(r"""\b(day before yesterday|day after tomorrow|yesterday|tomorrow|today)\b""",
                                    re.IGNORECASE): self.__extract_day,
                         re.compile(r'\b(next|in)* ?(\d+|a) (year|month|week|day)s? ?(ago|back)*\b',
                                    re.IGNORECASE): self.__extract_relative_days,
                         re.compile(r'\b(last|next) (year|month|week)\b',
                                    re.IGNORECASE): self.__extract_last_next,
                         re.compile(r'\b(last|next) (monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
                                    re.IGNORECASE): self.__extract_last_next_day,
                         }

        if ref:
            self.today = ref.date()
        else:
            self.today = datetime.date.today()

    def extract(self, text):
        """Extract all types of relative patterns."""
        result = []
        for pattern, functor in self.patterns.items():
            matches = pattern.findall(text)
            result.extend(functor(matches))

        return result

    def __extract_day(self, matches):
        """Extract today, tomorrow, yesterday, etc."""
        result = []
        one_day = datetime.timedelta(days=1)
        yesterday = self.today - one_day
        tomorrow = self.today + one_day
        db_yesterday = yesterday - one_day
        da_tomorrow = tomorrow + one_day

        for match in matches:
            match_lower = match.lower()
            if match_lower == 'yesterday':
                result.append(yesterday)
            elif match_lower == 'tomorrow':
                result.append(tomorrow)
            elif match_lower == 'today':
                result.append(self.today)
            elif match_lower == 'day before yesterday':
                result.append(db_yesterday)
            elif match_lower == 'day after tomorrow':
                result.append(da_tomorrow)

        return result

    def __extract_relative_days(self, matches):
        """Extract phrases like "in N days", "N days ago", etc."""
        result = []
        for match in matches:
            if match[1] == 'a':
                # For "in a week", "a week back", "a week ago", etc.
                if match[0] == 'next':
                    # "next a week" doesn't make sense
                    continue
                else:
                    num = 1
            else:
                # in N days, N weeks back, N years ago, etc.
                num = int(match[1])

            if match[2] == 'day':
                delta = datetime.timedelta(days=num)
            elif match[2] == 'week':
                delta = datetime.timedelta(weeks=num)
            elif match[2] == 'month':
                # assuming 30 days to a month
                delta = datetime.timedelta(days=num*30)
            elif match[2] == 'year':
                # assuming 365 days to a year
                delta = datetime.timedelta(days=num*365)

            if match[0] and match[3]:  # both in and ago doesn't make sense
                continue

            if match[0]:  # either of next or in
                result.append(self.today + delta)
            elif match[3]:  # either ago or back
                result.append(self.today - delta)

        return result

    def __extract_last_next(self, matches):
        """Extract from matches like last/next week/month/year combinations."""
        result = []
        for match in matches:
            if match[1] == 'week':
                delta = datetime.timedelta(weeks=1)
            elif match[1] == 'month':
                delta = datetime.timedelta(days=30)
            elif match[1] == 'year':
                delta = datetime.timedelta(days=365)

            if match[0] == 'last':
                result.append(self.today - delta)
            elif match[0] == 'next':
                result.append(self.today + delta)
        return result

    def __extract_last_next_day(self, matches):
        """Extract matches with last wednesday, next friday, etc."""
        result = []
        today_num = self.today.weekday()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_num = dict([(day, i) for i, day in enumerate(days)])
        for match in matches:
            match_num = day_num[match[1].lower()]
            if match[0] == 'last':
                if today_num >= match_num:
                    if today_num - match_num == 0: # matched day is also today
                        delta = datetime.timedelta(days=7)
                    else:
                        delta = datetime.timedelta(days=today_num - match_num)
                else:
                    delta = datetime.timedelta(days=7-today_num)
                result.append(self.today - delta)
            elif match[0] == 'next':
                if today_num >= match_num:
                    delta = datetime.timedelta(days=7 + match_num - today_num)
                else:
                    delta = datetime.timedelta(match_num - today_num)
                result.append(self.today + delta)
        return result
