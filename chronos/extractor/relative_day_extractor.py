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
                         re.compile(r'\b(next|in)* ?(\d+|a) (week|day)s? ?(ago|back)*\b',
                                    re.IGNORECASE): self.__extract_relative_days}

    def extract(self, text):
        """Extract all types of relative patterns."""
        result = []
        for pattern, functor in self.patterns.items():
            matches = pattern.findall(text)
            result.extend(functor(matches))

        return result

    @staticmethod
    def __extract_day(matches):
        """Extract today, tomorrow, yesterday, etc."""
        result = []
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        yesterday = today - one_day
        tomorrow = today + one_day
        db_yesterday = yesterday - one_day
        da_tomorrow = tomorrow + one_day

        for match in matches:
            match_lower = match.lower()
            if match_lower == 'yesterday':
                result.append(yesterday)
            elif match_lower == 'tomorrow':
                result.append(tomorrow)
            elif match_lower == 'today':
                result.append(today)
            elif match_lower == 'day before yesterday':
                result.append(db_yesterday)
            elif match_lower == 'day after tomorrow':
                result.append(da_tomorrow)

        return result

    @staticmethod
    def __extract_relative_days(matches):
        """Extract phrases like "in N days", "N days ago", etc."""
        result = []
        today = datetime.date.today()

        for match in matches:
            try:
                num = int(match[1])
            except ValueError:
                if match[1] == 'a' and match[0] != 'next':
                    num = 1
                else:
                    continue
            if match[2] == 'day':
                delta = datetime.timedelta(days=num)
            elif match[2] == 'week':
                delta = datetime.timedelta(weeks=num)

            if match[0] and match[3]:  # both in and ago doesn't make sense
                continue

            if match[0]:  # either of next or in
                result.append(today + delta)
            elif match[3]:  # either ago or back
                result.append(today - delta)

        return result