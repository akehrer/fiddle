# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

from PyQt4.QtTest import QTest
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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

    def test_drag_drop_file(self):
        """
        Test dropping multiple files on the tab widget.
        :return:

        http://stackoverflow.com/questions/11500844/qtest-its-possible-to-test-dragdrop
        http://wiki.qt.io/Drag_and_Drop_of_files
        """
        #
        pre_cnt = self.form.documents_tabWidget.count()
        # D&D events take MIME data and for files need URLs
        mime_files = QMimeData()
        files = [QUrl('file://../data/lorem.txt'),
                 QUrl('file://../data/utf8_text.txt')]
        mime_files.setUrls(files)
        # Drag the files
        action = Qt.MoveAction
        target = self.form.documents_tabWidget.rect().center()
        drag_drop = QDropEvent(target, action, mime_files, Qt.LeftButton, Qt.NoModifier)
        drag_drop.acceptProposedAction()
        # Drop the files
        self.form.documents_tabWidget.dropEvent(drag_drop)
        QTest.qWait(200)  # Give the GUI time to load the data
        # Check the number of tabs
        post_cnt = self.form.documents_tabWidget.count()
        self.assertGreater(post_cnt, pre_cnt)

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
