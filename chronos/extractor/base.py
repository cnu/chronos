#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Extractor(object):
    """Base class for all extractors

    Create a subclass of this Extractor class and implement the extract method.
    Should return a list of extracted result.
    """
    def extract(self, text):
        raise NotImplementedError

