# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import unittest
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from fiddle.controllers.Editors import *
from tests import FiddleTestFixture
from tests.helpers import *


class FiddleFiletypesTest(FiddleTestFixture):
    def test_unicode_open_saveas(self):
        srcpath = os.path.join(self.data_dir, 'utf8_test.txt')
        destpath = os.path.join(self.this_dir, 'utf8_test_temp.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        tab._write_file(destpath)
        desthash = sha_hash_file(destpath)
        self.assertEqual(srchash, desthash)
        os.remove(destpath)

    def test_win1252_open_saveas(self):
        srcpath = os.path.join(self.data_dir, 'win1252_test.txt')
        destpath = os.path.join(self.this_dir, 'win1252_test_temp.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        tab._write_file(destpath)
        desthash = sha_hash_file(destpath)
        self.assertEqual(srchash, desthash)
        os.remove(destpath)

    def test_pyfile_open(self):
        srcpath = os.path.join(self.data_dir, 'server.py')
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.assertIsInstance(tab.editor, PythonEditor)

    def test_jsfile_open(self):
        srcpath = os.path.join(self.data_dir, 'main.js')
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.assertIsInstance(tab.editor, JavascriptEditor)

    def test_htmlfile_open(self):
        srcpath = os.path.join(self.data_dir, 'index.html')
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.assertIsInstance(tab.editor, HTMLEditor)

    def test_cssfile_open(self):
        srcpath = os.path.join(self.data_dir, 'main.css')
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.assertIsInstance(tab.editor, CSSEditor)


if __name__ == "__main__":
    unittest.main()
