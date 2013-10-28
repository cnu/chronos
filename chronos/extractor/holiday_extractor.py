#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract holidays like christmas, new year or other popularly known days."""

import re
import datetime

from chronos.extractor.base import Extractor


class ChristmasExtractor(Extractor):
    """Extract Christmas or Christmas Eve from text."""
    def __init__(self):
        # Have patterns for last/next christmas
        self.pattern = re.compile(r"\b(christmas(\seve)*)\b", re.IGNORECASE)

    def extract(self, text):
        matches = self.pattern.findall(text)
        if not matches:
            return []
        
        # Get current year
        # TODO: Use a reference year
        cur_year = datetime.datetime.today().year

        result = []
        for match in matches:
            if len(match[0]) == 13: # christmas eve
                date_obj = datetime.date(cur_year, 12, 24)
            elif len(match[0]) == 9: # christmas
                date_obj = datetime.date(cur_year, 12, 25)

            result.append(date_obj)

        return result


class NewYearExtractor(Extractor):
    """Extract New Year or New Year Eve from text."""
    def __init__(self):
        # Have patterns for last/next christmas
        self.pattern = re.compile(r"\b(new\s?year'?s?(\seve)*)\b", re.IGNORECASE)

    def extract(self, text):
        matches = self.pattern.findall(text)
        if not matches:
            return []
        
        # Get current year
        # TODO: Use a reference year
        cur_year = datetime.date.today().year
        next_year = cur_year + 1

        result = []
        for match in matches:
            if match[-1]: # new years "eve"
                date_obj = datetime.date(cur_year, 12, 31)
            else: # just new years
                date_obj = datetime.date(next_year, 1, 1)

            result.append(date_obj)

        return result


__all__ = ['ChristmasExtractor', 'NewYearExtractor']