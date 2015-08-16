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

        # Default to UTF-8 encoding
        self.setUtf8(True)

        # Margin is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        margin_width = '0' * (line_num_margin + 1)
        self.setMarginWidth(0, fontmetrics.width(margin_width))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor(EDITOR_MARGIN_COLOR))

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
