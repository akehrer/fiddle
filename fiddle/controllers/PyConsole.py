# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import unicodedata
from io import StringIO

from PyQt4 import QtCore, QtGui
from fiddle.config import EDITOR_FONT, EDITOR_FONT_SIZE


class PyConsoleTextBrowser(QtGui.QTextBrowser):
    def __init__(self, parent=None, process=None):
        super(PyConsoleTextBrowser, self).__init__(parent)

        self.process = process

        # The start position in the QTextBrowser document where new user input will be inserted
        self._input_insert_pos = -1

        self.history = []
        self.history_idx = 0

        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        self.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextEditorInteraction)

    def keyPressEvent(self, event):
        if self.process is not None:
            # Skip keys modified with Ctrl or Alt
            if event.modifiers() != QtCore.Qt.ControlModifier and event.modifiers() != QtCore.Qt.AltModifier:
                # Get the insert cursor and make sure it's at the end of the console
                cursor = self.textCursor()
                cursor.movePosition(QtGui.QTextCursor.End)
                if self._input_insert_pos < 0:
                    self._input_insert_pos = cursor.position()

                # Scroll view to end of console
                self.setTextCursor(cursor)
                self.ensureCursorVisible()

                # Process the key event
                if event.key() == QtCore.Qt.Key_Up:
                    # Clear any previous input
                    self._clear_insert_line(cursor)
                    # Get the history
                    if len(self.history) > 0:
                        self.history_idx -= 1
                        try:
                            cursor.insertText(self.history[self.history_idx])
                        except IndexError:
                            self.history_idx += 1
                            cursor.insertText('')
                elif event.key() == QtCore.Qt.Key_Down:
                    # Clear any previous input
                    self._clear_insert_line(cursor)
                    # Get the history
                    if len(self.history) > 0 >= self.history_idx:
                        self.history_idx += 1
                        try:
                            cursor.insertText(self.history[self.history_idx])
                        except IndexError:
                            self.history_idx -= 1
                            cursor.insertText('')
                elif event.key() == QtCore.Qt.Key_Return:
                    txt = self._select_insert_line(cursor)
                    self.process.write('{0}\n'.format(txt).encode('utf-8'))
                    # Reset the insert position
                    self._input_insert_pos = -1
                    # Update the history
                    self.history.append(txt)
                    self.history_idx = 0
        # Pass the event on to the parent for handling
        return QtGui.QTextBrowser.keyPressEvent(self, event)

    def _clear_insert_line(self, cursor):
        """
        Remove all the displayed text from the input insert line and clear the input buffer
        """
        cursor.setPosition(self._input_insert_pos, QtGui.QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

    def _select_insert_line(self, cursor):
        cursor.setPosition(self._input_insert_pos, QtGui.QTextCursor.KeepAnchor)
        txt = cursor.selectedText()
        cursor.clearSelection()
        return txt


class PyConsoleLineEdit(QtGui.QLineEdit):
    """
    https://wiki.python.org/moin/PyQt/Adding%20tab-completion%20to%20a%20QLineEdit
    http://www.saltycrane.com/blog/2008/01/how-to-capture-tab-key-press-event-with/
    """
    def __init__(self):
        super(PyConsoleLineEdit, self).__init__()

        line_font = QtGui.QFont()
        line_font.setFamily(EDITOR_FONT)
        line_font.setPointSize(EDITOR_FONT_SIZE)
        self.setFont(line_font)

        self.history = []
        self.history_idx = -1

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:
                if self.text().strip() == '':
                    self.setText(self.text() + '    ')
                return True
            elif event.key() == QtCore.Qt.Key_Up:
                if len(self.history) > 0 and self.history_idx > 0:
                    self.history_idx -= 1
                    self.setText(self.history[self.history_idx])
                return True
            elif event.key() == QtCore.Qt.Key_Down:
                if 0 < len(self.history) > self.history_idx:
                    self.history_idx += 1
                    try:
                        self.setText(self.history[self.history_idx])
                    except IndexError:
                        self.setText('')
                return True
            elif event.key() == QtCore.Qt.Key_Return:
                try:
                    if self.history[-1] != self.text():
                        self.history.append(self.text())
                except IndexError:
                    self.history.append(self.text())
                self.history_idx = len(self.history)
                return QtGui.QLineEdit.event(self, event)

        return QtGui.QLineEdit.event(self, event)
