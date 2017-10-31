#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, unittest, tempfile, json, subprocess, shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from domovoi import Domovoi # noqa

class TestDomovoi(unittest.TestCase):
    def test_basic_statements(self):
        subprocess.check_call(["chalice", "new-project", "testproject"])
        readme_filename = os.path.join(os.path.dirname(__file__), "..", "README.rst")
        with open(readme_filename) as readme_fh, open("testproject/app.py", "w") as app_fh:
            for line in readme_fh.readlines():
                if line.strip() == ".. code-block:: python":
                    app_fh.write("# Domovoi test\n")
                elif "state_machine_definition" in line:
                    break
                elif app_fh.tell():
                    app_fh.write(line[4:])

        subprocess.check_call(["domovoi", "--dry-run", "deploy"], cwd="testproject")

    def test_state_machine(self):
        subprocess.check_call(["chalice", "new-project", "sfn"])
        shutil.copy(os.path.join(os.path.dirname(__file__), "..", "domovoi", "examples", "state_machine_app.py"),
                    os.path.join("sfn", "app.py"))
        subprocess.check_call(["domovoi", "--dry-run", "deploy"], cwd="sfn")


if __name__ == '__main__':
    unittest.main()
