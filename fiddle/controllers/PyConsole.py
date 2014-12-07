import subprocess
import sys
import telnetlib
from code import InteractiveConsole
from io import StringIO

from PyQt4 import QtCore, QtGui

from fiddle.utils import std_redirector
from fiddle.config import CONSOLE_HOST, CONSOLE_PORT, CONSOLE_PYTHON, CONSOLE_SCRIPT


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


class PyConsoleServer(QtCore.QThread):
    def __init__(self, host=CONSOLE_HOST, port=CONSOLE_PORT, cwd=None):
        super(PyConsoleServer, self).__init__()

        self.host = host
        self.port = port

        self._cwd = cwd
        self.process = None

    def __del__(self):
        self.wait()

    def stop(self):
        if self.process is not None:
            self.process.kill()

    def run(self):
        args = [CONSOLE_PYTHON, CONSOLE_SCRIPT, self.host, self.port]
        print(' '.join(args))
        self.process = subprocess.Popen(args, cwd=self._cwd, shell=False)


class PyConsoleClient(QtCore.QThread):
    data_ready = QtCore.pyqtSignal(str)

    def __init__(self, host, port):
        super(PyConsoleClient, self).__init__()

        self.host = host
        self.port = int(port)
        self._is_running = False

        self.telnet = None

    def stop(self):
        if self._is_running:
            self._is_running = False
            self.telnet.close()

    def run(self):
        self.telnet = telnetlib.Telnet(self.host, self.port)  # open the port
        self._is_running = True
        while self._is_running:
            try:
                data = self.telnet.read_until(b'\n', 0.1)  # basic readlines
                if len(data) > 0:
                    self.data_ready.emit(data.decode('utf8'))
            except EOFError:
                print('Error: PyConsole closed!')
                self._is_running = False
            except:
                pass

    def send(self, data):
        if self._is_running:
            command = '{}\n'.format(data)
            self.telnet.write(bytes(command, 'utf8'))


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
