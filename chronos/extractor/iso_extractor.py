#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract date & time formatted using ISO 8601 format."""

import re
import datetime

from chronos.extractor.base import Extractor


class ISO8601Extractor(Extractor):
    """Extract date/time formatted in ISO 8601 standard."""

    def __init__(self, ref=None):
        super(ISO8601Extractor, self).__init__(ref)
        self.load_patterns()

    def load_patterns(self):
        """Load a list of possible patterns to check the text for.

        Patterns should be loaded in the longest first order
        so that text containing date & time are found before text containing
        just date.
        """
        # Using pattern from http://stackoverflow.com/a/8270148/1448
        self.pattern = re.compile(r"""(
                                        \d{4}\-\d\d\-\d\d  # date
                                        ([tT][\d:\.]*)?    # optional time
                                      )
                                   """, re.VERBOSE)

    def extract(self, text):
        """Extract ISO formatted dates and time."""
        result = []
        matches = self.pattern.findall(text)

        for match in matches:
            # Use the right strptime format to parse it
            if len(match[0]) == 10: # YYYY-MM-DD
                fmt = "%Y-%m-%d"
            elif len(match[0]) == 13: # YYYY-MM-DDThh
                fmt = "%Y-%m-%dT%H"
            elif len(match[0]) == 16: # YYYY-MM-DDThh:mm
                fmt = "%Y-%m-%dT%H:%M"
            elif len(match[0]) == 19: # YYYY-MM-DDThh:mm:ss
                fmt = "%Y-%m-%dT%H:%M:%S"
            result.append(datetime.datetime.strptime(match[0], fmt))

        return result