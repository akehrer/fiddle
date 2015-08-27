# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from tests import FiddleTestFixture
from tests.helpers import *


class FiddleFindReplaceTest(FiddleTestFixture):
    findtext = 'abhorreant'
    replacetext = 'tnaerrohba'

    def test_find_text_return(self):
        """
        Test using the Return key to cycle through found elements in the test text and wrap around at EOF.
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        self.form.ui.findPane.show()
        self.form.ui.find_text_lineEdit.setText(self.findtext)
        QTest.keyClick(self.form.ui.find_text_lineEdit, Qt.Key_Return)
        first_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        QTest.keyClick(self.form.ui.find_text_lineEdit, Qt.Key_Return)
        second_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        self.assertNotEqual(first_pos, second_pos)
        # Wrap...
        QTest.keyClick(self.form.ui.find_text_lineEdit, Qt.Key_Return)
        wrap_pos = tab.editor.getCursorPosition()
        self.assertEqual(first_pos, wrap_pos)

    def test_find_text_next(self):
        """
        Test using the Next button to cycle through found elements in the test text and wrap around at EOF.
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        self.form.ui.findPane.show()
        self.form.ui.find_text_lineEdit.setText(self.findtext)
        QTest.mouseClick(self.form.ui.find_next_Button, Qt.LeftButton)
        first_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        QTest.mouseClick(self.form.ui.find_next_Button, Qt.LeftButton)
        second_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        self.assertNotEqual(first_pos, second_pos)
        # Wrap...
        QTest.mouseClick(self.form.ui.find_next_Button, Qt.LeftButton)
        wrap_pos = tab.editor.getCursorPosition()
        self.assertEqual(first_pos, wrap_pos)

    def test_find_text_previous(self):
        """
        Test using the Previous button to cycle through found elements in the test text and wrap around at EOF. The
        search should wrap immediately and start from the end of the file.
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        self.form.ui.findPane.show()
        self.form.ui.find_text_lineEdit.setText(self.findtext)
        # Wrap...
        QTest.mouseClick(self.form.ui.find_previous_Button, Qt.LeftButton)
        first_pos = tab.editor.getCursorPosition()  # (line, col) tuple
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        QTest.mouseClick(self.form.ui.find_previous_Button, Qt.LeftButton)
        second_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        self.assertNotEqual(first_pos, second_pos)
        self.assertGreater(first_pos[0], second_pos[0])  # Started from end of file
        QTest.mouseClick(self.form.ui.find_previous_Button, Qt.LeftButton)
        wrap_pos = tab.editor.getCursorPosition()
        self.assertEqual(first_pos, wrap_pos)

    def test_replace_text(self):
        """
        Test using the Replace button to cycle through found elements and replace them.
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        self.form.ui.findPane.show()
        self.form.ui.find_text_lineEdit.setText(self.findtext)
        self.form.ui.replace_text_lineEdit.setText(self.replacetext)
        # Find first instance
        QTest.mouseClick(self.form.ui.replace_Button, Qt.LeftButton)
        first_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        # Replace it an move to the next
        QTest.mouseClick(self.form.ui.replace_Button, Qt.LeftButton)
        self.assertEqual(tab.editor.selectedText(), self.findtext)
        second_pos = tab.editor.getCursorPosition()
        self.assertNotEqual(first_pos, second_pos)
        # Replace it and wrap (nothing found so don't change selection)
        QTest.mouseClick(self.form.ui.replace_Button, Qt.LeftButton)
        third_pos = tab.editor.getCursorPosition()
        self.assertEqual(tab.editor.selectedText(), self.replacetext)
        self.assertEqual(second_pos, third_pos)

    def test_replace_all_text(self):
        """
        Test using the Replace All button to cycle through all found elements and replace them.
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'lorem.txt')
        self.form.open_filepath(srcpath)
        tab = self.form.ui.documents_tabWidget.currentWidget()
        self.form.ui.findPane.show()
        self.form.ui.find_text_lineEdit.setText(self.findtext)
        self.form.ui.replace_text_lineEdit.setText(self.replacetext)
        QTest.mouseClick(self.form.ui.replace_all_Button, Qt.LeftButton)
        self.assertEqual(tab.editor.selectedText(), self.replacetext)
        # Try to find again (no text should be selected)
        QTest.mouseClick(self.form.ui.find_next_Button, Qt.LeftButton)
        self.assertEqual(tab.editor.selectedText(), '')
