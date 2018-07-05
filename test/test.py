#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, unittest, tempfile, json, subprocess, shutil, textwrap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from domovoi import Domovoi # noqa

class TestDomovoi(unittest.TestCase):
    def test_basic_statements(self):
        state_machine = {
            "StartAt": "Worker",
            "States": {
                "Worker": {
                    "Type": "Task",
                    "Resource": None,
                    "End": True
                }
            }
        }

        subprocess.check_call(["domovoi", "new-project", "testproject"])
        readme_filename = os.path.join(os.path.dirname(__file__), "..", "README.rst")
        with open(readme_filename) as readme_fh, open("testproject/app.py", "w") as app_fh:
            for line in readme_fh.readlines():
                if line.strip() == ".. code-block:: python":
                    app_fh.write("# Domovoi test\nstate_machine = {}\n".format(state_machine))
                elif line.strip() == "Installation":
                    break
                elif app_fh.tell():
                    app_fh.write(line[4:])

        subprocess.check_call(["domovoi", "--dry-run", "deploy"], cwd="testproject")

    def test_state_machine_examples(self):
        subprocess.check_call(["domovoi", "new-project", "testproject-sfn"])
        shutil.copy(os.path.join(os.path.dirname(__file__), "..", "domovoi", "examples", "state_machine_app.py"),
                    os.path.join("testproject-sfn", "app.py"))
        subprocess.check_call(["domovoi", "--dry-run", "deploy"], cwd="testproject-sfn")

    def test_state_machine_registration(self):
        sm_app = """
        import json, boto3, domovoi

        app = domovoi.Domovoi()

        def handler(event, context):
            pass

        state_machine = {
            "StartAt": "Worker",
            "States": {
                "Worker": {
                    "Type": "Task",
                    "Resource": handler,
                    "End": True
                }
            }
        }
        app.register_state_machine(state_machine)
        """

        subprocess.check_call(["domovoi", "new-project", "testproject2"])
        with open("testproject2/app.py", "w") as app_fh:
            app_fh.write(textwrap.dedent(sm_app))

        subprocess.check_call(["domovoi", "--dry-run", "deploy"], cwd="testproject2")


if __name__ == '__main__':
    unittest.main()
