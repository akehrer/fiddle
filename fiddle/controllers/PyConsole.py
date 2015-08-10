# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

from PyQt4 import QtCore, QtGui


class PyConsoleLineEdit(QtGui.QLineEdit):
    """
    https://wiki.python.org/moin/PyQt/Adding%20tab-completion%20to%20a%20QLineEdit
    http://www.saltycrane.com/blog/2008/01/how-to-capture-tab-key-press-event-with/
    """
    def __init__(self):
        super(PyConsoleLineEdit, self).__init__()
        self.setFrame(False)

        courier_font = QtGui.QFont()
        courier_font.setFamily("Courier")
        courier_font.setPointSize(10)
        self.setFont(courier_font)

    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Tab):
            if self.text().strip() == '':
                self.setText(self.text() + '    ')
            return True

        return QtGui.QLineEdit.event(self, event)