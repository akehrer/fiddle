# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from fiddle.controllers.MainWindow import MainWindow
from tests.helpers import *


class FiddleMainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.form = MainWindow()

        self.this_dir = os.path.dirname(__file__)
        self.files_dir = os.path.join(self.this_dir, 'files')

    def test_pyconsolelineedit_ascii(self):
        self.form.ui.pyConsole_output.clear()
        console_pre_txt = self.form.ui.pyConsole_output.toPlainText()

        self.form.pyconsole_input.setText("i = '{0}'".format(ICANEATGLASS['ascii']))
        QTest.keyClick(self.form.pyconsole_input, Qt.Key_Return)

        console_post_txt = self.form.ui.pyConsole_output.toPlainText()
        self.assertNotEqual(console_pre_txt, console_post_txt)
        self.assertTrue(ICANEATGLASS['ascii'] in console_post_txt)


if __name__ == "__main__":
    unittest.main()