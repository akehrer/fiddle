# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import logging
import os
import sys

# Import Qt modules
from PyQt4 import QtGui

# Import app modules
from fiddle.controllers.MainWindow import MainWindow
from fiddle.config import LOG_LEVEL

# Build the logger
logging.basicConfig(filename='fIDDLE.log',
                    filemode='a',
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=LOG_LEVEL)


class DumpStream():
    """
    A simple stream to dump all console I/O
    from: http://sebsauvage.net/python/snyppets/#py2exe
    """
    def __init__(self):
        pass

    def write(self, data):
        pass

    def read(self, data):
        pass

    def flush(self):
        pass

    def close(self):
        pass


class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)

        self.main = MainWindow()

        self.lastWindowClosed.connect(self.byebye)
        self.main.show()
        self.main.raise_()

    def byebye(self):
        self.main.stop()
        self.exit(0)


def set_dump_streams():
    sys.stdout = DumpStream()
    sys.stderr = DumpStream()
    sys.stdin = DumpStream()
    sys.__stdout__ = DumpStream()
    sys.__stderr__ = DumpStream()
    sys.__stdin__ = DumpStream()


def main():
    global app

    if LOG_LEVEL != logging.DEBUG:
        set_dump_streams()

    app = App(sys.argv)
    app.exec_()

if __name__ == "__main__":
    main()
