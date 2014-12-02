"""
A redirected code.InteractiveConsole from: http://evadeflow.com/2010/03/python-console-for-ig/
"""

import sys
from code import InteractiveConsole
from contextlib import contextmanager
from io import StringIO

from PyQt4 import QtCore, QtGui


@contextmanager
def std_redirector(stdin=sys.stdin, stdout=sys.stdin, stderr=sys.stderr):
    tmp_fds = stdin, stdout, stderr
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = tmp_fds
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds


class PyConsoleInterpreter(InteractiveConsole):
    def __init__(self, locals=None):
        super(PyConsoleInterpreter, self).__init__(locals)
        self.ps1 = getattr(sys, "ps1", ">>> ")
        self.ps2 = getattr(sys, "ps2", "... ")
        self.banner = ('Python {0} on {1}\n'
                       'Type "help", "copyright", "credits" or "license" '
                       'for more information.\n').format(sys.version, sys.platform)

    def push(self, command):
        output = StringIO()  # http://stackoverflow.com/questions/4330812/how-do-i-clear-a-stringio-object
        error = StringIO()
        with std_redirector(stdout=output, stderr=error):
            try:
                more = InteractiveConsole.push(self, command)
                result = output.getvalue()
                error = error.getvalue()
            except (SyntaxError, OverflowError):
                more = False
                result = ''
                error = ''
            return more, result, error


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
