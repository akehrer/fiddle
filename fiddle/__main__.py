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


def main():
    global app
    app = App(sys.argv)
    app.exec_()

if __name__ == "__main__":
    main()
