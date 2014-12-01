# Import standard library modules
import logging
import os
import sys

VERSION = '0.1'
PLATFORM = sys.platform
LOG_LEVEL = logging.DEBUG

# app directory, determine if application is a script file or frozen exe
# see: http://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
elif __file__:
    APP_DIR = os.path.dirname(__file__)

# Window title prefix
WINDOW_TITLE = 'fIDLE'

# Editor configuration
EDITOR_FONT = 'Courier'
EDITOR_FONT_SIZE = 10
EDITOR_MARGIN_COLOR = '#cccccc'
EDITOR_CARET_LINE_COLOR = '#ffffe0'
EDITOR_MARKER_COLOR = '#ee1111'

