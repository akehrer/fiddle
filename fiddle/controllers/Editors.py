# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)
# -------------------------------------------------------------------------
# Original QScintilla sample with PyQt from:
# Eli Bendersky (eliben@gmail.com)
#   This code is in the public domain
#   http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt
# -------------------------------------------------------------------------

from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciAPIs, QsciLexerPython, QsciLexerHTML, QsciLexerJavaScript, QsciLexerCSS

from fiddle.config import EDITOR_CARET_LINE_COLOR, EDITOR_FONT, EDITOR_FONT_SIZE, \
    EDITOR_MARGIN_COLOR, EDITOR_EDGECOL_COLOR


class BaseEditor(QsciScintilla):
    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(BaseEditor, self).__init__(parent)

        # Set the default font
        self.font = QFont()
        self.font.setFamily(EDITOR_FONT)
        self.font.setFixedPitch(True)
        self.font.setPointSize(EDITOR_FONT_SIZE)
        self.setFont(self.font)
        self.setMarginsFont(self.font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        margin_width = '0' * (line_num_margin + 1)
        self.setMarginWidth(0, fontmetrics.width(margin_width) + 5)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor(EDITOR_MARGIN_COLOR))

        # Edge Mode shows a gray vertical bar at 80 chars
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(QColor(EDITOR_EDGECOL_COLOR))

        # Fold code
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        # Brace matching: enable for a brace immediately before or after the current position
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(EDITOR_CARET_LINE_COLOR))

        # Use raw message to Scintilla here (all messages are documented here:
        # http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, bytearray(EDITOR_FONT, 'utf8'))
        self.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 1, EDITOR_FONT_SIZE)

        #self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)  # Hide the horizontal scrollbar
        self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)

        # Handle tabs properly
        self.setTabIndents(True)
        self.setTabWidth(4)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)

    def __repr__(self):
        return "<%s instance at %s>" % (self.__class__.__name__, id(self))

    def set_wordwrap(self, state):
        if state:
            self.setWrapMode(QsciScintilla.WrapWhitespace)
            self.setWrapVisualFlags(QsciScintilla.WrapFlagByBorder)
        else:
            self.setWrapMode(QsciScintilla.WrapNone)
            self.setWrapVisualFlags(QsciScintilla.WrapFlagNone)

    def set_whitespace(self, state):
        if state:
            self.setWhitespaceVisibility(QsciScintilla.WsVisible)
        else:
            self.setWhitespaceVisibility(QsciScintilla.WsInvisible)

    def set_eolchars(self, state):
        self.setEolVisibility(state)


class PythonEditor(BaseEditor):
    def __init__(self, parent=None, line_num_margin=3, autocomplete_list=None):
        super(PythonEditor, self).__init__(parent, line_num_margin, autocomplete_list)

        # Set Python lexer
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(self.font)
        # Set auto-completion
        self.api = QsciAPIs(self.lexer)
        if autocomplete_list is not None:
            # Add additional completion strings
            for i in autocomplete_list:
                self.api.add(i)
        self.api.prepare()
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setLexer(self.lexer)


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
        self.setAutoCompletionThreshold(2)
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
        self.setAutoCompletionThreshold(2)
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
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setLexer(self.lexer)
