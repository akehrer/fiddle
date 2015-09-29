# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)
import os
import sys
import urllib.parse
import subprocess

from PyQt4 import QtCore, QtGui
from fiddle.config import *


class PyConsoleProcessBrowser(QtGui.QTextBrowser):
    def __init__(self, parent=None, command='', args=None):
        super(PyConsoleProcessBrowser, self).__init__(parent)
        self.parent = parent

        # QProcess parameters
        self.process = QtCore.QProcess()
        self._command = ''
        self._command_dir = ''
        self._py_version = ''
        self._working_dir = ''
        self.args = [] if args is None else args
        self.command = command

        self.process.readyReadStandardError.connect(self._process_stderr)
        self.process.readyReadStandardOutput.connect(self._process_stdout)
        self.process.finished.connect(self._process_finished)

        # QTextbrowser parameters
        # The start position in the QTextBrowser document where new user input will be inserted
        self._input_insert_pos = -1

        self.history = []
        self.history_idx = 0

        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        self.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextEditorInteraction)

        # Base format
        self.base_format = self.currentCharFormat()
        self.base_format.setForeground(QtGui.QColor(CONSOLE_COLOR_BASE))

        # Error format for data on stderr
        self.error_format = QtGui.QTextCharFormat(self.base_format)
        self.error_format.setForeground(QtGui.QColor(CONSOLE_COLOR_ERROR))

        # Info format for data
        self.info_format = QtGui.QTextCharFormat(self.base_format)
        self.info_format.setForeground(QtGui.QColor(CONSOLE_COLOR_INFO))

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, cmd):
        if not cmd == self._command:
            # Update and restart
            self._command = cmd
            self._command_dir = os.path.dirname(cmd)

    @property
    def working_dir(self):
        if self._working_dir == '':
            self._working_dir = self.process.workingDirectory()
        return self._working_dir

    @working_dir.setter
    def working_dir(self, path_str):
        self._working_dir = path_str
        self.process.setWorkingDirectory(path_str)

    @property
    def py_version(self):
        if self._py_version == '':
            try:
                p = subprocess.Popen([self._command, '-c', 'import sys; print(sys.version)'],
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
                out, err = p.communicate(timeout=1)
                self._py_version = out.decode().strip()
            except subprocess.TimeoutExpired:
                self._py_version = ''
        return self._py_version

    def keyPressEvent(self, event):
        if self.process.state() == self.process.Running:
            # Skip keys modified with Ctrl or Alt
            if event.modifiers() != QtCore.Qt.ControlModifier and event.modifiers() != QtCore.Qt.AltModifier:
                # Get the insert cursor and make sure it's at the end of the console
                cursor = self.textCursor()
                if self._input_insert_pos < 0:
                    self._input_insert_pos = cursor.position()
                if cursor.position() < self._input_insert_pos:
                    # Handle left/right arrows
                    cursor.movePosition(QtGui.QTextCursor.End)

                # Scroll view to end of console
                self.setTextCursor(cursor)
                self.ensureCursorVisible()

                # Process the key event
                if event.key() == QtCore.Qt.Key_Up:
                    # Clear any previous input
                    self._clear_insert_line(cursor)
                    # Get the history
                    if len(self.history) > 0:
                        self.history_idx -= 1
                        try:
                            cursor.insertText(self.history[self.history_idx])
                        except IndexError:
                            self.history_idx += 1
                            cursor.insertText('')
                    return None
                elif event.key() == QtCore.Qt.Key_Down:
                    # Clear any previous input
                    self._clear_insert_line(cursor)
                    # Get the history
                    if len(self.history) > 0 >= self.history_idx:
                        self.history_idx += 1
                        try:
                            cursor.insertText(self.history[self.history_idx])
                        except IndexError:
                            self.history_idx -= 1
                            cursor.insertText('')
                elif event.key() == QtCore.Qt.Key_Return:
                    if not cursor.atEnd():
                        # User pressed return while in the middle of the line
                        cursor.movePosition(QtGui.QTextCursor.End)
                        self.setTextCursor(cursor)
                    txt = self._select_insert_line(cursor)
                    self.process.write('{0}\n'.format(txt).encode('utf-8'))
                    # Reset the insert position
                    self._input_insert_pos = -1
                    # Update the history
                    self.history.append(txt)
                    self.history_idx = 0
        # Pass the event on to the parent for handling
        return super(PyConsoleProcessBrowser, self).keyPressEvent(event)

    def restart(self):
        self.terminate()
        self.clear()
        self.run()

    def run(self):
        if self._command != '':
            if self._working_dir == '':
                self.process.setWorkingDirectory(self._command_dir)
            if len(self.args) > 0:
                self.process.start(self._command,  self.args)
            else:
                self.process.start(self._command)

    def terminate(self, timeout=5000):
        if self._command is not None and self.process.state() > 0:
            self._print_data_to_console('\n', self.info_format)
            self._print_data_to_console(self.tr('Python console is terminating...'), self.info_format)
            self.repaint()  # Force message to show
            self.process.write('exit()\n')
            self.process.close()
            if sys.platform == 'win32':
                self.process.kill()
            else:
                self.process.terminate()
                if not self.process.waitForFinished(timeout):
                    self.process.kill()

    def kill(self):
        """
        Kill the object's process
        :return:
        """
        self.terminate()

    def start(self, command, args=None):
        """
        Reimplement the behaviour or QProcess.start()
        :param command: string with path to the executable, or the full command to execute
        :param args: list of string argument to pass to the command
        :return:
        """
        self.command = command
        if args is not None:
            self.args = args
        else:
            self.args = []
        self.run()

    def _clear_insert_line(self, cursor):
        """
        Remove all the displayed text from the input insert line and clear the input buffer
        """
        cursor.setPosition(self._input_insert_pos, QtGui.QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

    def _select_insert_line(self, cursor):
        cursor.setPosition(self._input_insert_pos, QtGui.QTextCursor.KeepAnchor)
        txt = cursor.selectedText()
        cursor.clearSelection()
        return txt

    def _print_data_to_console(self, data, fmt, html=False):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        if html:
            cursor.insertHtml(data)
        else:
            cursor.insertText(data, fmt)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ensureCursorVisible()

    def _process_stderr_lines(self, lines, cursor):
        """
        Process lines from a Python interpreter stderr. For tracebacks additional information is added.

        :param list lines:
        :param QtGui.QTextCursor cursor:
        :return:

        Lines from stderr often contain traceback data. This function processes those lines and adds additional
        information to help the user troubleshoot. For example links are created to error documentation and to lines
        in source files where errors were raised. The output is entered on the text cursor provided by `cursor`.
        """
        for line in lines:
            line = line + os.linesep  # Line separators were stripped off in the split, add them back
            ll = line.lower()
            ls = line.strip()
            lsl = ls.lower()
            if 'error' in ll and ll[0] != ' ':
                # Information lines start with whitespace so they're not processed here
                m = CONSOLE_RE_ERROR.search(line)
                if m:
                    groups = m.groups()
                    error = groups[0]
                    try:
                        desc = line.split(error)
                        link = '<a href="help://?object={0}&text={1}">{2}</a>'.format(error,
                                                                                      urllib.parse.quote_plus(ls),
                                                                                      error)
                        if len(desc) > 1:
                            cursor.insertText(desc[0], self.error_format)
                            cursor.insertHtml(link)
                            cursor.insertText(''.join(desc[1:]), self.error_format)
                        else:
                            cursor.insertHtml(link)
                            cursor.insertText(''.join(desc), self.error_format)
                        cursor.insertText(os.linesep, self.base_format)
                    except ValueError:
                        cursor.insertText(line, self.error_format)
                else:
                    cursor.insertText(line, self.error_format)
            elif 'file' in lsl:
                m = CONSOLE_RE_LINENUM.search(line)
                if m:
                    groups = m.groups()
                    filepath = groups[1]
                    linenum = groups[3]
                    url_filepath = urllib.parse.quote_plus(filepath[1:-1])  # Strip leading and trailing quotes
                    if 'stdin' in filepath:
                        cursor.insertText(line, self.error_format)
                    else:
                        link = '<a href="goto://?filepath={0}&linenum={1}">{2}</a>&nbsp'.format(url_filepath,
                                                                                                int(linenum),
                                                                                                filepath)
                        cursor.insertText(groups[0], self.error_format)
                        cursor.insertHtml(link)
                        cursor.insertText(''.join(groups[2:]), self.error_format)
                else:
                    cursor.insertText(line, self.error_format)
            elif CONSOLE_PS1 in line:
                cursor.insertText(ls + ' ', self.base_format)
            elif CONSOLE_PS2 in line:
                cursor.insertText(ls + ' ', self.base_format)
            else:
                cursor.insertText(line, self.error_format)

    def _process_stdout(self):
        self.process.setReadChannel(QtCore.QProcess.StandardOutput)
        data = self.process.readAll()
        lines = data.data().decode().split(os.linesep)
        for line in lines:
            line = line + os.linesep  # Line separators were stripped off in the split, add them back
            # Create clickable links
            m = CONSOLE_RE_HTTP.findall(line)
            if m:
                linked = line
                for g in m:
                    linked = linked.replace(g, '<a href={0}>{0}</a>'.format(g))
                self._print_data_to_console(linked, self.base_format, html=True)
                self._print_data_to_console(os.linesep, self.base_format)
            else:
                self._print_data_to_console(line, self.base_format)

    def _process_stderr(self):
        self.process.setReadChannel(QtCore.QProcess.StandardError)
        data = self.process.readAll()
        lines = data.data().decode().split(os.linesep)
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self._process_stderr_lines(lines, cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ensureCursorVisible()

    def _process_finished(self, code):
        self.insertPlainText(os.linesep)
        self.insertPlainText(self.tr('Exited with code {0}').format(code))
        self.ensureCursorVisible()
        self.process.close()
