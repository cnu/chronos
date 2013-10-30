#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract date & time from text having today, tomorrow, yesterday, etc."""

import re
import datetime

from chronos.extractor.base import Extractor


class RelativeDayExtractor(Extractor):

    def __init__(self, ref=None):
        super(RelativeDayExtractor, self).__init__(ref)
        self.pattern = re.compile(r"""\b(day before yesterday|day after tomorrow|yesterday|tomorrow|today)\b""",
                                  re.IGNORECASE)

    def extract(self, text):
        """Extract ISO formatted dates and time."""
        result = []
        matches = self.pattern.findall(text)

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