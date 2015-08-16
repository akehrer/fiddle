# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import os
import json
import logging

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import application modules
from fiddle.views.ManageInterpretersDialog import Ui_manageInterpreters_Dialog

from fiddle.config import PLATFORM, APP_DIR, CONSOLE_PYTHON, CONSOLE_PYTHON_INTERPRETERS

# Set up the logger
logger = logging.getLogger(__name__)


class ManageInterpretersDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ManageInterpretersDialog, self).__init__()

        self.parent = parent

        self.ui = Ui_manageInterpreters_Dialog()
        self.ui.setupUi(self)

        self.temp_interpreters = CONSOLE_PYTHON_INTERPRETERS

        self.py_icon = QtGui.QIcon()
        self.py_icon.addPixmap(QtGui.QPixmap(":/icons/icons/python_twosnakes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pyvenv_icon = QtGui.QIcon()
        self.pyvenv_icon.addPixmap(QtGui.QPixmap(":/icons/icons/python_twosnakes_v.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.init_default_interpreter()
        self.init_elements()

        # Catch changes in the order of items
        self.ui.pyInterpreters_List.model().layoutChanged.connect(self.update_temp_interpreters)

    def init_default_interpreter(self):
        # Add system interpreter
        self.ui.defaultInterpreterPath_label.setText('(Default) ' + CONSOLE_PYTHON)

    def init_elements(self):
        # Add user interpreters
        self.ui.pyInterpreters_List.clear()
        for item in self.temp_interpreters:
            w = QtGui.QListWidgetItem()
            w.setText(item)
            w.setIcon(self.py_icon)
            self.ui.pyInterpreters_List.addItem(w)

    def add_interpreter(self):
        filepath = QtGui.QFileDialog.getOpenFileName(None,
                                                     None,
                                                     '/',
                                                     'python.exe' if PLATFORM == 'win32' else 'python')
        if filepath != '':
            self.temp_interpreters.append(filepath)
            self.init_elements()

    def remove_interpreter(self):
        item = self.ui.pyInterpreters_List.takeItem(self.ui.pyInterpreters_List.currentRow())
        del item
        self.update_temp_interpreters()

    def update_temp_interpreters(self):
        self.temp_interpreters = []
        for i in range(self.ui.pyInterpreters_List.count()):
            self.temp_interpreters.append(self.ui.pyInterpreters_List.item(i).text())