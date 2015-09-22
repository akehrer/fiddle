# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import json
import logging
import os
import re
import subprocess
import sys

PLATFORM = sys.platform
LOG_LEVEL = logging.DEBUG

ABOUT_FIDDLE = """
Copyright (c) 2015 Aaron Kehrer
Licensed under the terms of the MIT License

Created using Python and PyQT

Silk icons CC-BY Mark James

See the LICENSE file for additional license information
"""


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


# Determine if application is a script file or frozen exe
# see: http://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
# also up the logging level to INFO for frozen app
APP_DIR = os.path.dirname(os.path.realpath(__file__))
APP_FROZEN = False
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    LOG_LEVEL = logging.INFO
    APP_FROZEN = True


# App file types
FILE_TYPES = ['fiddle Files (*.py *.html *.htm *.js *.css)',
              'Python Files (*.py)',
              'HTML Files (*.html *.htm)',
              'Javascript Files (*.js)',
              'CSS Files (*.css)',
              'All Files (*.*)']

# Editor configuration
if PLATFORM == 'win32':
    EDITOR_FONT = 'Consolas'
    EDITOR_FONT_SIZE = 10
    WINDOW_FONT_SIZE = 15
elif PLATFORM == 'darwin':
    EDITOR_FONT = 'Menlo'
    EDITOR_FONT_SIZE = 12
    WINDOW_FONT_SIZE = 13
else:
    EDITOR_FONT = 'DejaVu Sans Mono'
    EDITOR_FONT_SIZE = 12
    WINDOW_FONT_SIZE = 15

EDITOR_MARGIN_COLOR = '#cccccc'
EDITOR_EDGECOL_COLOR = '#dddddd'
EDITOR_CARET_LINE_COLOR = '#ffffe0'

# Window title prefix
WINDOW_TITLE = 'fiddle'

# MainWindow Stylesheet
WINDOW_STYLE = """
QMainWindow {
    background-color: white;
}

QWidget {
  /* Applies to all the widgets */
  font-family: "Segoe UI", "Lucida Grande", sans-serif;
  font-size: %spx;
}

QFrame {
  background-color: white;
}

QTextBrowser {
  font-family: "Consolas", "Menlo", "Monaco", "DejaVu Sans Mono", monospace, fixed;
}

QFrame QToolButton {
  background-color: white;
}

QTabWidget::pane {
  background-color: white;
}

QDockWidget::title {
  text-align: left;
  background: whitesmoke;
  padding: 7px;
}

QDockWidget::close-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 0px; right: 10px; bottom: 0px;
    width: 14px;
}

QDockWidget QToolButton {
  background-color: white;
}
""" % WINDOW_FONT_SIZE

# Python Console Configuration
CONSOLE_HOST = '127.0.0.1'
CONSOLE_PYTHON = {'path': find_python_exe(), 'virtualenv': False}
CONSOLE_PYTHON_DIR = os.path.dirname(CONSOLE_PYTHON['path'])
CONSOLE_PS1 = getattr(sys, "ps1", ">>> ")
CONSOLE_PS2 = getattr(sys, "ps2", "... ")
CONSOLE_HELP_PORT = 7464

# Console colors
CONSOLE_COLOR_BASE = "#000000"
CONSOLE_COLOR_ERROR = "#990000"
CONSOLE_COLOR_INFO = "#000099"

# Console RegEx
CONSOLE_RE_PYVER = re.compile(r'.*?(\d)\.(\d)\.(\d)', re.IGNORECASE|re.DOTALL)
CONSOLE_RE_LINENUM = re.compile(r'(\s+File\s+)(".*")(.\s+line\s+)(\d+)(.*)', re.IGNORECASE|re.DOTALL)
CONSOLE_RE_ERROR = re.compile(r'([A-Za-z]+Error)', re.IGNORECASE|re.DOTALL)
CONSOLE_RE_HTTP = re.compile(r'(https?://[^\s/$.?#].[^\s\'\"]*)', re.IGNORECASE|re.DOTALL)  # based on @stephenhay

# Help Configuration
try:
    with open('searchers.json') as fp:
        HELP_WEB_SEARCH_SOURCES = json.load(fp)
except (ValueError, FileNotFoundError):
    HELP_WEB_SEARCH_SOURCES = [{'name': 'Google',
                                'query_tmpl': 'https://www.google.com/search?q={query}'}]

# Python Interpreters Configuration
try:
    with open('interpreters.json') as fp:
        CONSOLE_PYTHON_INTERPRETERS = json.load(fp)
except (ValueError, FileNotFoundError):
    CONSOLE_PYTHON_INTERPRETERS = []
