# Import standard library modules
import logging
import os
import subprocess
import sys

VERSION = '0.1'
PLATFORM = sys.platform
LOG_LEVEL = logging.DEBUG


def find_python_exe():
    """
    Find the path to the system's Python executable
    :return: str
    """
    try:
        if PLATFORM == 'win32':
            p = subprocess.check_output(['where', 'python'])
        else:
            p = subprocess.check_output(['which', 'python'])
        return p.strip().decode('utf8')
    except subprocess.CalledProcessError:
        return ''

# app directory, determine if application is a script file or frozen exe
# see: http://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
# also up the logging level to INFO for frozen app
APP_DIR = os.path.dirname(__file__)
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    LOG_LEVEL = logging.INFO


# Window title prefix
WINDOW_TITLE = 'fIDDLE'

# Editor configuration
EDITOR_FONT = 'Courier'
EDITOR_FONT_SIZE = 10
EDITOR_MARGIN_COLOR = '#cccccc'
EDITOR_CARET_LINE_COLOR = '#ffffe0'
EDITOR_MARKER_COLOR = '#ee1111'

# Python Console Configuration
CONSOLE_HOST = '127.0.0.1'
CONSOLE_PORT = '3000'
CONSOLE_PYTHON = find_python_exe()
CONSOLE_SCRIPT = os.path.join(APP_DIR, 'scripts', 'console_server.py')
CONSOLE_PS1 = getattr(sys, "ps1", ">>> ")
CONSOLE_PS2 = getattr(sys, "ps2", "... ")

# Help Configuration
HELP_GOOGLE_URL = 'https://www.google.com/search?q={query}'


