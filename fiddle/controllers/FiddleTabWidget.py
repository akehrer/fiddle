# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import os

# Import additional modules
import chardet

from PyQt4 import QtCore, QtGui

from fiddle.controllers.Editors import *
from fiddle.config import FILE_TYPES, PLATFORM

# An iterator to update as the user creates new files
new_file_iter = 1


class FiddleTabWidget(QtGui.QWidget):
    editor_changed = QtCore.pyqtSignal()
    cursor_changed = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None, filepath=None):
        super(FiddleTabWidget, self).__init__(parent)

        self._filepath = None
        self._saved = True

        self.basepath = None
        self.filename = None
        self.extension = None
        self.encoding = 'utf-8'  # Default to UTF-8 encoding

        # Set the layout and insert the editor
        self.editor = None
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setMargin(0)
        self.layout().setSpacing(0)

        # Find/Replace
        self.find_expr = ''
        self.find_forward = False
        self.found_first = False

        self.filepath = filepath
        self.watcher = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, path):
        global new_file_iter
        if path is not None:
            self._filepath = path
            self.basepath, self.filename = os.path.split(path)
            _, ext = os.path.splitext(path)
            self.extension = ext.lower()

            with open(path, 'rb') as fp:
                data = fp.read()
            enc = chardet.detect(data)['encoding']
            self.encoding = enc if enc is not None else 'utf-8'

            if '.htm' in self.extension:
                self.insert_editor(HTMLEditor(parent=self))
            elif self.extension == '.js':
                self.insert_editor(JavascriptEditor(parent=self))
            elif self.extension == '.css':
                self.insert_editor(CSSEditor(parent=self))
            elif self.extension == '.py':
                self.insert_editor(PythonEditor(parent=self))
            else:
                self.insert_editor(BaseEditor(parent=self))

            try:
                self.editor.setText(data.decode(self.encoding))
            except TypeError:
                self.editor.setText('')
            self._saved = True
        else:
            self.basepath = None
            self.filename = 'new_{}.py'.format(new_file_iter)
            self.extension = '.py'
            self._filepath = os.path.join(os.path.expanduser('~'), self.filename)
            self.insert_editor(PythonEditor(parent=self))
            new_file_iter += 1
            self._saved = False

    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, state):
        self._saved = state
        self.editor_changed.emit()

    def insert_editor(self, editor):
        if self.editor is not None and self.layout().indexOf(self.editor) >= 0:
            self.layout().removeWidget(self.editor)
            self.editor.deleteLater()
            self.editor = None
        self.editor = editor
        self.editor.textChanged.connect(self._set_text_changed)
        self.editor.cursorPositionChanged.connect(self._cursor_position_changed)
        self.layout().addWidget(self.editor)

    def save(self):
        if self.basepath is None:
            self.save_as()
        else:
            self._write_file(self.filepath)
            self.saved = True

    def save_as(self):
        path = self.basepath or os.path.join(os.path.expanduser('~'), self.filename)
        filepath = QtGui.QFileDialog.getSaveFileName(None, None, path, ';;'.join(FILE_TYPES[1:]))
        if filepath is not '':
            self._write_file(filepath)
            self.filepath = filepath
            self.saved = True

    def find_text(self, expr, re, cs, wo, wrap,
                  in_select=False, forward=True, line=-1, index=-1, show=True, posix=False):
        """
        Find the string expr and return true if expr was found, otherwise returns false.
        If expr is found it becomes the current selection. This is a convenience function around the find features
        built in to QsciScintilla.

        http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html

        :param expr:
        :param re:
        :param cs:
        :param wo:
        :param wrap:
        :param in_select:
        :param forward:
        :param line:
        :param index:
        :param show:
        :param posix:
        :return:
        """
        # Check for new expression
        if expr != self.find_expr:
            self.find_expr = expr
            self.found_first = False

        # Check for change in direction
        if forward != self.find_forward:
            if self.editor.hasSelectedText():
                line, idx, _, _ = self.editor.getSelection()
                self.editor.setCursorPosition(line, idx)
            self.find_forward = forward
            self.found_first = False

        if self.found_first:
            return self.editor.findNext()
        elif in_select:
            res = self.editor.findFirstInSelection(expr, re, cs, wo, forward, show, posix)
            if res:
                self.found_first = True
                return True
            else:
                self.found_first = False
                return False
        else:
            res = self.editor.findFirst(expr, re, cs, wo, wrap, forward, line, index, show, posix)
            if res:
                self.found_first = True
                return True
            else:
                self.found_first = False
                return False

    def replace_text(self, old_expr, new_text, re, cs, wo, wrap,
                     in_select=False, forward=True, line=-1, index=-1, show=True, posix=False):
        if self.found_first:
            # Replace the text and move to the next occurrence
            self.editor.replace(new_text)
            self.editor.findNext()
        else:
            # Find the first occurrence
            self.find_text(old_expr, re, cs, wo, wrap, in_select, forward, line, index, show, posix)

    def replace_all_text(self, old_expr, new_text, re, cs, wo, in_select=False):
        i = 0
        if in_select:
            if self.editor.findFirstInSelection(old_expr, re, cs, wo, False):
                self.editor.replace(new_text)
                i = 1
                while self.editor.findNext():
                    self.editor.replace(new_text)
                    i += 1
        else:
            # Start from the beginning of the document and work to the end
            if self.editor.findFirst(old_expr, re, cs, wo, False, True, 0, 0):
                self.editor.replace(new_text)
                i = 1
                while self.editor.findNext():
                    self.editor.replace(new_text)
                    i += 1
        return i

    def _write_file(self, filepath):
        with open(filepath, 'wb') as fp:
            fp.write(bytes(self.editor.text(), self.encoding))

    def _set_text_changed(self):
        self.editor.autoCompleteFromAll()
        self.saved = False

    def _cursor_position_changed(self, line, idx):
        self.cursor_changed.emit(line, idx)
