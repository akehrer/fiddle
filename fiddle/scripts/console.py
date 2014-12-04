import json
import socket
import sys
from code import InteractiveConsole

if sys.version_info[0] == 3:
    from io import StringIO as _BytesIO
else:
    from io import BytesIO as _BytesIO


class PyConsoleInterpreter(InteractiveConsole, object):
    def __init__(self, locals=None):
        super(PyConsoleInterpreter, self).__init__(locals)
        self.ps1 = getattr(sys, "ps1", ">>> ")
        self.ps2 = getattr(sys, "ps2", "... ")
        self.banner = ('Python {0} on {1}\n'
                       'Type "help", "copyright", "credits" or "license" '
                       'for more information.\n').format(sys.version, sys.platform)

    def push(self, command):
        output = _BytesIO()  # http://stackoverflow.com/questions/4330812/how-do-i-clear-a-stringio-object
        error = _BytesIO()
        orig_fds = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = output, error
            more = InteractiveConsole.push(self, command)
            result = output.getvalue()
            error = error.getvalue()
        except (SyntaxError, OverflowError):
            more = False
            result = ''
            error = ''
        finally:
            sys.stdout, sys.stderr = orig_fds
        return json.dumps([more, result, error])

if __name__ == '__main__':
    ic = PyConsoleInterpreter()
