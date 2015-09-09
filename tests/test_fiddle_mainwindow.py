# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import QWidget, QMessageBox, QPushButton

from tests import app, FiddleTestFixture
from tests.helpers import *


class FiddleMainWindowTest(FiddleTestFixture):
    def test_close_tab_discard(self):
        dh = DiscardHelper()
        # Open the file
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        self.assertTrue(tab.saved)
        # Modify the file
        QTest.keyClick(tab.editor, Qt.Key_Return)
        QTest.keyClick(tab.editor, Qt.Key_Return)
        self.assertFalse(tab.saved)
        # Close the tab and discard the changes
        pre_cnt = self.form.ui.documents_tabWidget.count()
        QTimer.singleShot(200, dh.click_discard)
        self.form.close_tab(1)
        post_cnt = self.form.ui.documents_tabWidget.count()
        self.assertNotEqual(pre_cnt, post_cnt)


class DiscardHelper(QWidget):
    def __init__(self):
        super(DiscardHelper, self).__init__()

    def click_discard(self):
        widgets = app.topLevelWidgets()
        for w in widgets:
            if type(w) is QMessageBox:
                btns = w.findChildren(QPushButton)
                for b in btns:
                    if b.text().lower() == 'discard':
                        QTest.mouseClick(b, Qt.LeftButton)
