# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

from PyQt4 import QtCore, QtGui
from fiddle.config import EDITOR_FONT, EDITOR_FONT_SIZE


class PyConsoleLineEdit(QtGui.QLineEdit):
    """
    https://wiki.python.org/moin/PyQt/Adding%20tab-completion%20to%20a%20QLineEdit
    http://www.saltycrane.com/blog/2008/01/how-to-capture-tab-key-press-event-with/
    """
    def __init__(self):
        super(PyConsoleLineEdit, self).__init__()
        self.setFrame(False)

        courier_font = QtGui.QFont()
        courier_font.setFamily(EDITOR_FONT)
        courier_font.setPointSize(EDITOR_FONT_SIZE)
        self.setFont(courier_font)

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
