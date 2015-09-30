# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import os
import json
import logging

# Import Qt modules
from PyQt4 import QtGui

# Import application modules
from fiddle.views.ManageInterpretersDialog import Ui_manageInterpreters_Dialog

from fiddle.config import CONSOLE_PYTHON, WINDOW_STYLE
from fiddle.helpers import check_virtualenv, get_python_version

# Set up the logger
logger = logging.getLogger(__name__)


class ManageInterpretersDialog(QtGui.QDialog):
    def __init__(self, parent=None, interpreters=None):
        super(ManageInterpretersDialog, self).__init__(parent)

        self.parent = parent

        self.ui = Ui_manageInterpreters_Dialog()
        self.ui.setupUi(self)
        self.setStyleSheet(WINDOW_STYLE)

        self.temp_interpreters = [] if interpreters is None else interpreters

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
        self.ui.defaultInterpreterPath_label.setText('(Default) ' + CONSOLE_PYTHON['path'])

    def init_elements(self):
        # Add user interpreters
        self.ui.pyInterpreters_List.clear()
        for item in self.temp_interpreters:
            w = QtGui.QListWidgetItem()
            w.setText(item['path'])
            w.setData(32, item)
            if item['virtualenv']:
                w.setIcon(self.pyvenv_icon)
            else:
                w.setIcon(self.py_icon)
            self.ui.pyInterpreters_List.addItem(w)

    def add_interpreter(self):
        filepath = QtGui.QFileDialog.getOpenFileName(None,
                                                     None,
                                                     '/',
                                                     'Python Interpreters (python* ipython*)')
        if filepath != '':
            # Check for executable
            if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                interpreter = {'path': filepath,
                               'virtualenv': check_virtualenv(filepath),
                               'version': get_python_version(filepath)}
                self.temp_interpreters.append(interpreter)
                self.init_elements()

    def remove_interpreter(self):
        item = self.ui.pyInterpreters_List.takeItem(self.ui.pyInterpreters_List.currentRow())
        del item
        self.update_temp_interpreters()

    def update_temp_interpreters(self):
        new_order = []
        for i in range(self.ui.pyInterpreters_List.count()):
            new_order.append(self.ui.pyInterpreters_List.item(i).data(32))
        self.temp_interpreters = new_order
