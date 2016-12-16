#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, unittest, tempfile, json, subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from domovoi import Domovoi

class TestDomovoi(unittest.TestCase):
    def test_basic_statements(self):
        subprocess.check_call(["chalice", "new-project", "testproject"])

if __name__ == '__main__':
    unittest.main()
