# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import logging
import os
import re
import subprocess
import sys

VERSION = '0.1'
PLATFORM = sys.platform
LOG_LEVEL = logging.DEBUG

ABOUT_FIDDLE = """
Copyright (c) 2015 Aaron Kehrer
Licensed under the terms of the MIT License

Created using Python and PyQT

Silk icons CC-BY Mark James
http://www.famfamfam.com/lab/icons/silk/
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
APP_DIR = os.path.dirname(__file__)
APP_FROZEN = False
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    LOG_LEVEL = logging.INFO
    APP_FROZEN = True


# Window title prefix
WINDOW_TITLE = 'fIDDLE'

# Editor configuration
EDITOR_FONT = 'Courier'
EDITOR_FONT_SIZE = 10
EDITOR_MARGIN_COLOR = '#cccccc'
EDITOR_EDGECOL_COLOR = '#dddddd'
EDITOR_CARET_LINE_COLOR = '#ffffe0'

# Python Console Configuration
CONSOLE_HOST = '127.0.0.1'
CONSOLE_PYTHON = find_python_exe()
CONSOLE_PYTHON_DIR = os.path.dirname(CONSOLE_PYTHON)
CONSOLE_PS1 = getattr(sys, "ps1", ">>> ")
CONSOLE_PS2 = getattr(sys, "ps2", "... ")
CONSOLE_HELP_PORT = 7464

# Console colors
CONSOLE_COLOR_BASE = "#000000"
CONSOLE_COLOR_ERROR = "#990000"
CONSOLE_COLOR_INFO = "#000099"

# Console RegEx
CONSOLE_RE_PYVER = re.compile(r'.*?(\d)\.(\d)\.(\d)', re.IGNORECASE|re.DOTALL)
CONSOLE_RE_LINENUM = re.compile(r'(\s+File\s+)(".*?")(.\s+line\s+)(\d+)(.\sin\s)(.+)', re.IGNORECASE|re.DOTALL)

# Help Configuration
HELP_WEB_SEARCH_SOURCES = [('Google', 'https://www.google.com/search?q={query}'),
                           ('DuckDuckGo', 'https://duckduckgo.com/?q={query}')]



