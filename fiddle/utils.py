
import subprocess
import sys
from contextlib import contextmanager
from io import StringIO

from fiddle.config import PLATFORM


@contextmanager
def std_redirector(stdin=sys.stdin, stdout=sys.stdin, stderr=sys.stderr):
    tmp_fds = stdin, stdout, stderr
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = tmp_fds
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds


def find_python_exe():
    try:
        if PLATFORM == 'win32':
            p = subprocess.check_output(['where', 'python'])
        else:
            p = subprocess.check_output(['which', 'python'])
        return p.strip().decode('utf8')
    except subprocess.CalledProcessError:
        return ''
