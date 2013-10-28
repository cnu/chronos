#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime


class Extractor(object):
    def extract(self, text):
        raise NotImplementedError


class ISODateTimeExtractor(Extractor):
    def extract(self, text):
        pass


class ChristmasExtractor(Extractor):
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
                d = datetime.date(cur_year, 12, 24)
            elif len(match[0]) == 9: # christmas
                d = datetime.date(cur_year, 12, 25)

            result.append(d)

        return result
