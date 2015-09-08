# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import unittest
from string import ascii_letters, digits, punctuation

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from fiddle.controllers.ManageInterpretersDialog import ManageInterpretersDialog
from fiddle.config import CONSOLE_PYTHON

from tests import FiddleTestFixture
from tests.helpers import *


class FiddleInterpretersTest(FiddleTestFixture):
    def test_open_interpreters_dialog(self):
        mi_dialog = ManageInterpretersDialog(self.form)
        self.assertIn(CONSOLE_PYTHON['path'], mi_dialog.ui.defaultInterpreterPath_label.text())
