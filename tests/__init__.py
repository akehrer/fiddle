# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import sys
import unittest
import sip
from PyQt4.QtGui import QApplication

from fiddle.controllers.MainWindow import MainWindow

sip.setdestroyonexit(False)
app = QApplication(sys.argv)


class FiddleTestFixture(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.form = MainWindow(app=app)
        self.this_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.this_dir, 'data')

    def tearDown(self):
        self.form.stop()