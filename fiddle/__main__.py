# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import argparse
import logging
import os
import sys

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import app modules
from fiddle.controllers.MainWindow import MainWindow
from fiddle.config import *

# Build the logger
logging.basicConfig(filename='fIDDLE.log',
                    filemode='a',
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=LOG_LEVEL)

# Commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*')


class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        pargs = parser.parse_args()

        self.main = MainWindow(self, files=pargs.files)
        self.main.setStyleSheet(WINDOW_STYLE)

        self.aboutToQuit.connect(self.byebye)
        self.main.show()
        self.main.raise_()

    def byebye(self):
        self.main.stop()
        self.exit(0)


def main():
    app = App(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(QtCore.QLocale.system().name() + '.qm', 'locale')
    app.exec_()

if __name__ == "__main__":
    main()
