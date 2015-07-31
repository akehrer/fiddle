# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import os

from PyQt4 import QtCore, QtGui

from fiddle.controllers.SimplePythonEditor import SimplePythonEditor

# An iterator to update as the user creates new files
new_file_iter = 1


class FIdleTabWidget(QtGui.QWidget):
    editor_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None, filepath=None):
        super(FIdleTabWidget, self).__init__(parent)

        self._filepath = None
        self._saved = True

        self.basepath = None
        self.filename = None

        self.editor = SimplePythonEditor()
        self.filepath = filepath


        # Set the layout and insert the editor
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setMargin(0)
        self.layout().addWidget(self.editor)

        self.editor.textChanged.connect(self._set_text_changed)

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, path):
        global new_file_iter
        try:
            self._filepath = path
            self.basepath, self.filename = os.path.split(path)
            with open(path) as fp:
                self.editor.setText(fp.read())
            self._saved = True
        except TypeError:
            self.basepath = None
            self.filename = 'new_{}.py'.format(new_file_iter)
            cwd = os.getcwd()
            self._filepath = os.path.join(cwd, self.filename)
            new_file_iter += 1
            self._saved = False

    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, state):
        self._saved = state
        self.editor_changed.emit()

    def _set_text_changed(self):
        self.saved = False