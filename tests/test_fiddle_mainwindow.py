# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import unittest
from string import ascii_letters, digits, punctuation
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from fiddle.controllers.MainWindow import MainWindow
from tests.helpers import *


app = QApplication(sys.argv)


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

    def test_unicode_open_saveas(self):
        srcpath = os.path.join(self.data_dir, 'utf8_test.txt')
        destpath = os.path.join(self.this_dir, 'utf8_test_temp.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        tab._write_file(destpath)
        desthash = sha_hash_file(destpath)
        self.assertEqual(srchash, desthash)
        os.remove(destpath)

    def test_win1252_open_saveas(self):
        srcpath = os.path.join(self.data_dir, 'win1252_test.txt')
        destpath = os.path.join(self.this_dir, 'win1252_test_temp.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        tab._write_file(destpath)
        desthash = sha_hash_file(destpath)
        self.assertEqual(srchash, desthash)
        os.remove(destpath)

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
