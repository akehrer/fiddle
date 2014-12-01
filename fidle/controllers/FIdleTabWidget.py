# Import standard library modules
import os

from PyQt4 import QtCore, QtGui

from fidle.controllers.SimplePythonEditor import SimplePythonEditor

# An iterator to update as the user creates new files
new_file_iter = 1


class FIdleTabWidget(QtGui.QWidget):
    editor_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None, filepath=None):
        super(FIdleTabWidget, self).__init__(parent)
        global new_file_iter

        self.filepath = filepath
        self.editor = SimplePythonEditor()

        try:
            self.filename = os.path.basename(filepath)
            with open(filepath) as fp:
                self.editor.setText(fp.read())
            self.saved = True
        except TypeError:
            self.filename = 'new_{}.py'.format(new_file_iter)
            new_file_iter += 1
            self.saved = False

        # Set the layout and insert the editor
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setMargin(0)
        self.layout().addWidget(self.editor)

        self.editor.textChanged.connect(self._set_text_changed)

    def _set_text_changed(self):
        self.saved = False
        self.editor_changed.emit()