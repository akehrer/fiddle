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

    def test_pyconsolelineedit_ascii(self):
        self.form.ui.pyConsole_output.clear()
        console_pre_txt = self.form.ui.pyConsole_output.toPlainText()
        test_str = ascii_letters + digits + punctuation
        self.form.pyconsole_input.setText("i = '{0}'".format(test_str))
        QTest.keyClick(self.form.pyconsole_input, Qt.Key_Return)

        console_post_txt = self.form.ui.pyConsole_output.toPlainText()
        self.assertNotEqual(console_pre_txt, console_post_txt)
        self.assertTrue(test_str in console_post_txt)

    def test_pyconsolelineedit_history(self):
        self.form.ui.pyConsole_output.clear()
        test_strs = [ascii_letters, digits, punctuation]
        # Load the history
        for ts in test_strs:
            self.form.pyconsole_input.setText("i = '{0}'".format(ts))
            QTest.keyClick(self.form.pyconsole_input, Qt.Key_Return)

        # Check up arrow against history
        self.assertEqual('', self.form.pyconsole_input.text())
        for ts in reversed(test_strs):
            QTest.keyClick(self.form.pyconsole_input, Qt.Key_Up)
            self.assertEqual("i = '{0}'".format(ts), self.form.pyconsole_input.text())

        # Check down arrow agaist history
        for ts in test_strs[1:]:
            QTest.keyClick(self.form.pyconsole_input, Qt.Key_Down)
            self.assertEqual("i = '{0}'".format(ts), self.form.pyconsole_input.text())

        # Last down arrow should clear the input
        QTest.keyClick(self.form.pyconsole_input, Qt.Key_Down)
        self.assertEqual('', self.form.pyconsole_input.text())

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
