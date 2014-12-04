"""
A redirected code.InteractiveConsole from: http://evadeflow.com/2010/03/python-console-for-ig/
A non-blocking stream reader from: http://eyalarubas.com/python-subproc-nonblock.html
"""

import subprocess
import sys
from threading import Thread
from queue import Queue, Empty
from code import InteractiveConsole
from io import StringIO

from PyQt4 import QtCore, QtGui

from fiddle.utils import std_redirector


class PyConsoleServer(QtCore.QThread):
    def __init__(self, pypath, srcpath, cwd=None):
        super(PyConsoleServer, self).__init__()

        self.python_path = pypath
        self.server_script = srcpath
        self.cwd = cwd
        self.process = None

    def __del__(self):
        self.wait()

    def stop(self):
        if self.process is not None:
            self.process.kill()

    def run(self):
        args = [self.python_path, self.server_script]
        print(' '.join(args))
        self.process = subprocess.Popen(args, cwd=self.cwd, shell=False)


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


class PyConsoleInterpreter2():
    def __init__(self, pypath):
        super(PyConsoleInterpreter2, self).__init__()
        self.ps1 = getattr(sys, "ps1", ">>> ")
        self.ps2 = getattr(sys, "ps2", "... ")

        args = [pypath, '-m', "code"]  # Start an InteractiveConsole

        self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        shell=False, bufsize=0, universal_newlines=True)
        self.stream_out = StreamThread(self.process.stdout)
        self.stream_err = StreamThread(self.process.stderr)
        # self.create_console_object()

    def create_console_object(self):
        self.process.stdin.write('from code import InteractiveConsole\n')
        self.process.stdin.write('ic = InteractiveConsole()\n')
        # self.process.stdin.write('ic.push("i")\n')

    def push(self, command, timeout=0.1):
        self.process.stdin.write('{}\n'.format(command))


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


class StreamThread(QtCore.QThread):
    new_line = QtCore.pyqtSignal(str)

    def __init__(self, stream):
        super(StreamThread, self).__init__()

        self.stream = stream
        self.is_running = True

    def __del__(self):
        self.wait()

    def stop(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            data = self.stream.readline()
            if data:
                self.new_line.emit(data)


class NonBlockingStreamReader():

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target=_populateQueue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout=None):
        try:
            return self._q.get(block=timeout is not None, timeout=timeout)
        except Empty:
            return None


class UnexpectedEndOfStream(Exception): pass