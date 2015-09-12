# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

from PyQt4.QtTest import QTest

from tests import FiddleTestFixture
from tests.helpers import *


class FiddleMainWindowTest(FiddleTestFixture):
    def test_clean_code(self):
        """
        Can a file with poor PEP8 formatting be cleaned with better formatting?
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'unclean.py')
        cleanpath = os.path.join(self.data_dir, 'cleaned.py')
        with open(cleanpath, 'rb') as fp:
            clean_data = fp.read().decode()
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.assertNotEqual(tab.editor.text(), clean_data)
        self.form.ui.actionClean_Code.trigger()
        self.assertEqual(tab.editor.text(), clean_data)

    def test_check_code(self):
        """
        Can quality issues in code be flagged for review by the user?
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'unlinted.py')
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.form.ui.actionCheck_Code.trigger()
        QTest.qWait(200)
        next_marker = tab.editor.markerFindNext(0,-1)
        self.assertGreater(next_marker, -1)