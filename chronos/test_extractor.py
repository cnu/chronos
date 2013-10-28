#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from extractor import Extractor


class BaseExtractorTestCase(unittest.TestCase):
    def test_base_extract(self):
        ext = Extractor()
        self.assertRaises(NotImplementedError, ext.extract, '')


if __name__ == '__main__': # pragma: no cover
    unittest.main()
