#!/usr/bin/env python
# -*- coding: utf-8 -*-

from extractor import *

extractors = [e() for e in Extractor.__subclasses__()]


def parse(text):
    """Parse a string and return a list of dictionaries with date & time info."""
    if not text:
        return []

    result = []
    for extractor in extractors:
        out = extractor.extract(text)
        if out:
            result.extend(out)

    return result

