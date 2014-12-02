# -------------------------------------------------------------------------
#
# QScintilla sample with PyQt
#
# Original from:
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
# http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt
# -------------------------------------------------------------------------
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

from fiddle.config import EDITOR_CARET_LINE_COLOR, \
    EDITOR_FONT, EDITOR_FONT_SIZE, EDITOR_MARGIN_COLOR, \
    EDITOR_MARKER_COLOR


class SimplePythonEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None, line_num_margin=2):
        super(SimplePythonEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily(EDITOR_FONT)
        font.setFixedPitch(True)
        font.setPointSize(EDITOR_FONT_SIZE)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        margin_width = '0' * (line_num_margin + 1)
        self.setMarginWidth(0, fontmetrics.width(margin_width) + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor(EDITOR_MARGIN_COLOR))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.connect(self, SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'), self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor(EDITOR_MARKER_COLOR), self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(EDITOR_CARET_LINE_COLOR))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)

        # Use raw message to Scintilla here (all messages are documented here:
        # http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, bytearray('Courier', 'utf8'))
        self.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, 1, EDITOR_FONT_SIZE)

        # Don't want to see the horizontal scrollbar at all
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # Handle tabs properly
        self.setTabIndents(True)
        self.setTabWidth(4)
        self.setAutoIndent(True)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
