#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .extractor import *


def parse(text, ref=None):
    """Parse a string and return list of dictionaries with date & time info."""
    if not text:
        return []

    extractors = [e(ref) for e in Extractor.__subclasses__()]

    result = []
    for extractor in extractors:
        out = extractor.extract(text)
        if out:
            result.extend(out)

    return result

