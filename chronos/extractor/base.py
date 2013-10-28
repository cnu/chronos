#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Extractor(object):
    """Base class for all extractors

    Create a subclass of this Extractor class and implement the extract method.
    Should return a list of extracted result.
    """
    def __init__(self, ref=None):
        """Initialize with a reference datetime object.

        All extractors will use this reference datetime for any relative dates.
        The current datetime will be set to ref and any calculations be done.
        """
        self.ref = ref

    def extract(self, text):
        raise NotImplementedError

