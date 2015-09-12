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
        """
        Test closing a tab with unsaved data. The changes are discarded.
        Note: Modal will flash...
        :return:
        """
        # Open the file
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        srchash = sha_hash_file(srcpath)
        self.form.open_filepath(srcpath)
        tab = self.form.documents_tabWidget.currentWidget()
        self.assertTrue(tab.saved)
        # Modify the file
        QTest.keyClick(tab.editor, Qt.Key_Return)
        QTest.keyClick(tab.editor, Qt.Key_Return)
        self.assertFalse(tab.saved)
        # Close the tab and discard the changes
        pre_cnt = self.form.documents_tabWidget.count()
        QTimer.singleShot(200, self._discard_dialog)
        self.form.close_tab(1)
        post_cnt = self.form.documents_tabWidget.count()
        self.assertNotEqual(pre_cnt, post_cnt)
        self.assertEqual(srchash, sha_hash_file(srcpath))

    def _discard_dialog(self):
        """
        Click the 'Discard' button on a modal dialog.
        This function is usually called by a QTimer that starts before the
        function that creates the dialog.

            QTimer.singleShot(200, self._discard_dialog)

        :return:
        """
        widgets = app.topLevelWidgets()
        for w in widgets:
            if type(w) is QMessageBox:
                btns = w.findChildren(QPushButton)
                for b in btns:
                    if b.text().lower() == 'discard':
                        QTest.mouseClick(b, Qt.LeftButton)
