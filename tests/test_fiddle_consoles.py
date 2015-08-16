# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import unittest
from string import ascii_letters, digits, punctuation

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from fiddle.controllers.MainWindow import MainWindow
from tests import app
from tests.helpers import *


class FiddleMainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.form = MainWindow(app=app)
        self.this_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.this_dir, 'data')

    def tearDown(self):
        self.form.stop()

    def test_no_console_restart(self):
        old_int = self.form.current_interpreter
        old_int_dir = self.form.current_interpreter_dir
        self.form.current_interpreter = ''
        self.form.current_interpreter_dir = ''
        self.form.restart_pyconsole_process()
        self.assertEqual('', self.form.ui.pyConsole_output.toPlainText())
        self.form.current_interpreter = old_int
        self.form.current_interpreter_dir = old_int_dir

    def test_no_help_restart(self):
        old_int = self.form.current_interpreter
        old_int_dir = self.form.current_interpreter_dir
        self.form.current_interpreter = ''
        self.form.current_interpreter_dir = ''
        self.form.restart_pyconsole_help()
        self.assertEqual('', self.form.ui.helpBrowser.page().mainFrame().toPlainText())
        self.form.current_interpreter = old_int
        self.form.current_interpreter_dir = old_int_dir


if __name__ == "__main__":
    unittest.main()