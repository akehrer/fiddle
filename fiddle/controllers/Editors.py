# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)
# -------------------------------------------------------------------------
# Original QScintilla sample with PyQt from:
# Eli Bendersky (eliben@gmail.com)
#   This code is in the public domain
#   http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt
# -------------------------------------------------------------------------

import os
import autopep8

from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciAPIs, QsciLexerPython, QsciLexerHTML, QsciLexerJavaScript, QsciLexerCSS

from fiddle.helpers import linter

from fiddle.config import EDITOR_CARET_LINE_COLOR, EDITOR_FONT, EDITOR_FONT_SIZE, \
    EDITOR_MARGIN_COLOR, EDITOR_EDGECOL_COLOR


class BaseEditor(QsciScintilla):
    editor_changed = QtCore.pyqtSignal()

    lintErrorMarkerNum = 8
    lintWarnMarkerNum = 9
    colorErrorForeground = '#a94442'
    colorErrorBackground = '#f2dede'
    colorWarnForeground = '#8a6d3b'
    colorWarnBackground = EDITOR_CARET_LINE_COLOR

    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(BaseEditor, self).__init__(parent)

        # Set the default font
        self.font = QFont()
        self.font.setFamily(EDITOR_FONT)
        self.font.setFixedPitch(True)
        self.font.setPointSize(EDITOR_FONT_SIZE)
        self.setFont(self.font)
        self.setMarginsFont(self.font)

        # Default to UTF-8 encoding
        self.setUtf8(True)

        # Margin is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        margin_width = '0' * (line_num_margin + 1)
        self.setMarginWidth(0, fontmetrics.width(margin_width))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor(EDITOR_MARGIN_COLOR))
        self.setMarginSensitivity(1, True)

        # Edge Mode shows a gray vertical bar  at the column set
        self._edgecol = 0
        self.setEdgeColor(QColor(EDITOR_EDGECOL_COLOR))

        # Fold code
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        # Brace matching: enable for a brace immediately before or after the current position
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(EDITOR_CARET_LINE_COLOR))

        # Use raw messages to Scintilla here
        # (all messages are documented here: http://www.scintilla.org/ScintillaDoc.html)
        # Ensure the width of the currently visible lines can be scrolled
        self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)

        # Linter
        self.linter = None  # Linter program to run, should be in the system's path
        self.lint_data = {}

        # Linter output markers
        self.marginClicked.connect(self.margin_clicked)
        self.lint_err_marker = self.markerDefine('!', self.lintErrorMarkerNum)
        self.setMarkerForegroundColor(QColor(self.colorErrorForeground), self.lint_err_marker)
        self.setMarkerBackgroundColor(QColor(self.colorErrorBackground), self.lint_err_marker)
        self.lint_warn_marker = self.markerDefine('?', self.lintWarnMarkerNum)
        self.setMarkerForegroundColor(QColor(self.colorWarnForeground), self.lint_warn_marker)
        self.setMarkerBackgroundColor(QColor(self.colorWarnBackground), self.lint_warn_marker)

        # Margin popup
        self._margin_popup = QWidget(self)
        self._margin_popup_lbl = QLabel(self._margin_popup)
        self._init_margin_popup()
        self._margin_popup_timer = QtCore.QTimer()
        self._margin_popup_timer.setSingleShot(True)
        self._margin_popup_timer.setInterval(2000)
        self._margin_popup_timer.timeout.connect(self._hide_margin_popup)

    def __repr__(self):
        return "<%s instance at %s>" % (self.__class__.__name__, id(self))

    @property
    def encoding(self):
        if self.isUtf8():
            return 'utf-8'
        else:
            return 'Latin1'
            
    @property
    def wordwrap(self):
        if self.wrapMode() == QsciScintilla.WrapWhitespace:
            return True
        else:
            return False
        
    @wordwrap.setter
    def wordwrap(self, state):
        if state:
            self.setWrapMode(QsciScintilla.WrapWhitespace)
            self.setWrapVisualFlags(QsciScintilla.WrapFlagByBorder)
        else:
            self.setWrapMode(QsciScintilla.WrapNone)
            self.setWrapVisualFlags(QsciScintilla.WrapFlagNone)
            
    @property
    def whitespace(self):
        if self.whitespaceVisibility() == QsciScintilla.WsVisible:
            return True
        else:
            return False

    @whitespace.setter
    def whitespace(self, state):
        if state:
            self.setWhitespaceVisibility(QsciScintilla.WsVisible)
        else:
            self.setWhitespaceVisibility(QsciScintilla.WsInvisible)

    @property
    def eolchars(self):
        return self.eolVisibility()
    
    @eolchars.setter
    def eolchars(self, state):
        self.setEolVisibility(state)
        
    @property
    def edgecol(self):
        return self._edgecol
    
    @edgecol.setter
    def edgecol(self, col):
        self._edgecol = col
        self.setEdgeColumn(col)
        if col > 0:
            self.setEdgeMode(QsciScintilla.EdgeLine)
        else:
            self.setEdgeMode(QsciScintilla.EdgeNone)

    def clean_code(self):
        """
        Runs a code cleaner to conform code to a certain style a la PEP8
        :return:
        """
        pass

    def check_code(self, path):
        """
        Runs a code linter to catch mistakes. This is usually an external program like Pylint.
        :param str path:
            File path to lint
        :return:
        """
        pass

    def margin_clicked(self, marnum, linenum, modifiers):
        """
        Slot that catches margin clicks. The linter puts error and warning markers in the margin
        :param int marnum: marker number in the list of markers (starting at 1)
        :param int linenum: line number where marker was clicked
        :param QtCore.KeyboardModifiers modifiers: any keyboard modifiers (Ctrl, Shift, Alt)
        :return:
        """
        pass

    def _clear_all_margin_markers(self):
        self.markerDeleteAll(-1)

    def _add_error_margin_marker(self, line):
        self.markerAdd(line, self.lint_err_marker)

    def _add_warn_margin_marker(self, line):
        self.markerAdd(line, self.lint_warn_marker)

    def _init_margin_popup(self):
        self._margin_popup_lbl.setText('')
        layout = QVBoxLayout(self._margin_popup)
        layout.addWidget(self._margin_popup_lbl)
        self._margin_popup.setLayout(layout)

        self._margin_popup.setWindowFlags(QtCore.Qt.Popup)
        self._margin_popup.setFocusPolicy(QtCore.Qt.NoFocus)
        self._margin_popup.setFocusProxy(self)

        self._margin_popup.setWindowOpacity(0.95)
        self._margin_popup.setStyleSheet('background-color:%s' % self.colorWarnBackground)

    def _show_margin_popup(self, msg, bg_color=EDITOR_CARET_LINE_COLOR):
        self._margin_popup_lbl.setText(msg)
        self._margin_popup.setStyleSheet('background-color:%s' % bg_color)
        self._margin_popup.move(QCursor.pos())
        self._margin_popup.setFocus()
        self._margin_popup.show()
        self._margin_popup_timer.start()

    def _hide_margin_popup(self):
        self._margin_popup.hide()


class PythonEditor(BaseEditor):
    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(PythonEditor, self).__init__(parent, line_num_margin, autocomplete_list)

        # Set Python lexer
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(self.font)
        self.lexer.setFont(self.font, QsciLexerPython.Comment)
        # Indentation warning ("The indentation is inconsistent when compared to the previous line")
        self.lexer.setIndentationWarning(QsciLexerPython.Inconsistent)
        # Set auto-completion
        self.api = QsciAPIs(self.lexer)
        if autocomplete_list is not None:
            # Add additional completion strings
            for i in autocomplete_list:
                self.api.add(i)
        self.api.prepare()
        self.setAutoCompletionThreshold(3)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setLexer(self.lexer)

        # PEP8 tabs
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        
        # PEP8 edge column line
        self.edgecol = 80

        # Linters
        self.linter = 'internal'

    def clean_code(self):
        self.setText(autopep8.fix_code(self.text(), options={'aggressive': 2}))

    def check_code(self, path):
        self._clear_all_margin_markers()
        self.lint_data = {}
        try:
            warnings = linter.check(self.text(), os.path.basename(path))
            for w in warnings:
                w.type = 'warning'
                key = w.lineno - 1
                if key in self.lint_data.keys():
                    self.lint_data[key].append(w)
                else:
                    self.lint_data[key] = [w]
                self._add_warn_margin_marker(w.lineno - 1)
        except linter.LinterSyntaxError as e:
            e.type = 'error'
            self.lint_data[e.lineno - 1] = e
            self._add_error_margin_marker(e.lineno - 1)
        except linter.LinterUnexpectedError as e:
            print(e)

    def margin_clicked(self, marnum, linenum, modifiers):
        if self._margin_popup.isVisible():
            self._hide_margin_popup()
        else:
            try:
                warnings = self.lint_data[linenum]
                desc = ''
                if isinstance(warnings, linter.LinterError):
                    desc = warnings.message
                    self._show_margin_popup(desc.strip(), bg_color=self.colorErrorBackground)
                else:
                    for warning in warnings:
                        desc += warning.message % warning.message_args + '\n'
                    self._show_margin_popup(desc.strip(), bg_color=self.colorWarnBackground)
            except KeyError:
                pass
        return True


class HTMLEditor(BaseEditor):
    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(HTMLEditor, self).__init__(parent, line_num_margin, autocomplete_list)

        # Set HTML lexer
        self.lexer = QsciLexerHTML(self)
        self.lexer.setDefaultFont(self.font)
        # Set auto-completion
        self.api = QsciAPIs(self.lexer)
        if autocomplete_list is not None:
            # Add additional completion strings
            for i in autocomplete_list:
                self.api.add(i)
        self.api.prepare()
        self.setAutoCompletionThreshold(3)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setLexer(self.lexer)


class JavascriptEditor(BaseEditor):
    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(JavascriptEditor, self).__init__(parent, line_num_margin, autocomplete_list)

        # Set HTML lexer
        self.lexer = QsciLexerJavaScript(self)
        self.lexer.setDefaultFont(self.font)
        # Set auto-completion
        self.api = QsciAPIs(self.lexer)
        if autocomplete_list is not None:
            # Add additional completion strings
            for i in autocomplete_list:
                self.api.add(i)
        self.api.prepare()
        self.setAutoCompletionThreshold(3)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setLexer(self.lexer)


class CSSEditor(BaseEditor):
    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(CSSEditor, self).__init__(parent, line_num_margin, autocomplete_list)

        # Set HTML lexer
        self.lexer = QsciLexerCSS(self)
        self.lexer.setDefaultFont(self.font)
        # Set auto-completion
        self.api = QsciAPIs(self.lexer)
        if autocomplete_list is not None:
            # Add additional completion strings
            for i in autocomplete_list:
                self.api.add(i)
        self.api.prepare()
        self.setAutoCompletionThreshold(3)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setLexer(self.lexer)
