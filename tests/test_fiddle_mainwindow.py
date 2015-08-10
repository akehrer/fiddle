# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import sys
import hashlib
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from fiddle.controllers.MainWindow import MainWindow
from tests.helpers import *


app = QApplication(sys.argv)


class FiddleMainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.form = MainWindow()
        self.this_dir = os.path.dirname(__file__)
        self.files_dir = os.path.join(self.this_dir, 'files')

    def tearDown(self):
        self.form.stop()

    def test_pyconsolelineedit_ascii(self):
        self.form.ui.pyConsole_output.clear()
        console_pre_txt = self.form.ui.pyConsole_output.toPlainText()

        self.form.pyconsole_input.setText("i = 'abcdefghijklmnopqrstuvwxyz'")
        QTest.keyClick(self.form.pyconsole_input, Qt.Key_Return)

        console_post_txt = self.form.ui.pyConsole_output.toPlainText()
        self.assertNotEqual(console_pre_txt, console_post_txt)
        self.assertTrue('abcdefghijklmnopqrstuvwxyz' in console_post_txt)

    def test_unicode_open_saveas(self):
        srcpath = os.path.join(self.files_dir, 'utf8_test.txt')
        destpath = os.path.join(self.this_dir, 'utf8_test_temp.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        tab._write_file(destpath)
        desthash = sha_hash_file(destpath)
        self.assertEqual(srchash, desthash)
        os.remove(destpath)

    def test_win1252_open_saveas(self):
        srcpath = os.path.join(self.files_dir, 'win1252_test.txt')
        destpath = os.path.join(self.this_dir, 'win1252_test_temp.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        tab._write_file(destpath)
        desthash = sha_hash_file(destpath)
        self.assertEqual(srchash, desthash)
        os.remove(destpath)

if __name__ == "__main__":
    unittest.main()