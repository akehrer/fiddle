# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import html
import logging
import os
import re
import subprocess
import time
import urllib.parse

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import application modules
from fiddle.views.MainWindow import Ui_MainWindow
from fiddle.controllers.FiddleTabWidget import FIdleTabWidget
from fiddle.controllers.PyConsole import PyConsoleServer, PyConsoleClient, PyConsoleLineEdit

from fiddle.config import WINDOW_TITLE, \
    CONSOLE_PS1, CONSOLE_PS2, CONSOLE_PYTHON, CONSOLE_HELP_PORT,\
    HELP_GOOGLE_URL

from fiddle.helpers.builtins import *

# Set up the logger
logger = logging.getLogger(__name__)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(WINDOW_TITLE)

        # Initialize actions
        self.init_menu_actions()

        # Hide the help pane
        self.ui.helpPane.hide()

        # Initialize Python console
        self.pyconsole_input = PyConsoleLineEdit()
        self.ui.pyconsole_prompt_layout.insertWidget(1, self.pyconsole_input)
        self.pyconsole_input.returnPressed.connect(self.send_pyconsole_command)
        self.ui.pyConsole_output.anchorClicked.connect(self.load_anchor)
        self.pyconsole_server = None
        self.pyconsole_client = None
        self.pyconsole_help = None
        self.pyconsole_traceback = []
        self.pyconsole_pyversion = None  # stores a tuple of the system Python's version
        self.start_pyconsole_server()
        self.start_pyconsole_client()
        self.start_pyconsole_help()

        # Store run script info
        self.runscript_path = None
        self.runscript_traceback = []

        # Add a blank file
        self.new_file()

    def stop(self):
        try:
            self.pyconsole_server.stop()
            self.pyconsole_server.quit()
            self.pyconsole_server.wait()
        except AttributeError:
            pass

        try:
            self.pyconsole_client.stop()
            self.pyconsole_client.quit()
            self.pyconsole_client.wait()
        except AttributeError:
            pass

        try:
            self.pyconsole_help.stop()
            self.pyconsole_help.quit()
            self.pyconsole_help.wait()
        except AttributeError:
            pass

    def init_menu_actions(self):
        # File actions
        self.ui.actionNew.triggered.connect(self.new_file)
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave_File.triggered.connect(self.save_file)
        self.ui.actionSave_File_As.triggered.connect(self.save_file_as)
        self.ui.actionPrint.triggered.connect(self.print_file)
        self.ui.actionClose_Tab.triggered.connect(self.close_current_tab)
        self.ui.actionClose_All_Tabs.triggered.connect(self.close_all_tabs)

        self.ui.actionExit.triggered.connect(self.exit_app)

        # Edit actions
        # TODO

        # Console actions
        # TODO
        self.ui.actionRun_Current_Script.triggered.connect(self.run_current_script)

        # Help actions
        self.ui.actionShow_Help_Pane.triggered.connect(self.show_help_pane)
        self.ui.actionHide_Help_Pane.triggered.connect(lambda x: self.ui.helpPane.hide())

    def init_open_recent(self):
        pass

    def start_pyconsole_server(self):
        # Start a server that serves InteractiveConsoles from the systems Python install
        self.pyconsole_server = PyConsoleServer()
        self.pyconsole_server.start()

    def start_pyconsole_client(self):
        # Start an interactive console
        self.pyconsole_client = PyConsoleClient(self.pyconsole_server.host, self.pyconsole_server.port)
        self.pyconsole_client.data_ready.connect(self._process_console_stdout)
        self.pyconsole_client.start()

    def start_pyconsole_help(self):
        # Start a second console that serves the pydoc help
        self.pyconsole_help = PyConsoleClient(self.pyconsole_server.host, self.pyconsole_server.port)
        self.pyconsole_help.data_ready.connect(lambda x: logger.debug(x))
        self.pyconsole_help.start()
        # Poll the server until the connection is up and running and then start the pydoc help server
        timeout = 100
        while True:
            if self.pyconsole_help.send('import pydoc'):
                break
            else:
                time.sleep(0.1)
                timeout -= 1
                if timeout < 0:
                    raise RuntimeError('Could not start the help server!')
        self.pyconsole_help.send('pydoc.serve({0})'.format(CONSOLE_HELP_PORT))

    def new_file(self):
        tab = FIdleTabWidget(parent=self.ui.documents_tabWidget)
        tab.editor_changed.connect(self.update_tab_title)
        tabname = tab.filename if tab.saved else tab.filename + ' *'
        idx = self.ui.documents_tabWidget.addTab(tab, tabname)
        self.ui.documents_tabWidget.setCurrentIndex(idx)

    def open_file(self):
        file_path = QtGui.QFileDialog.getOpenFileName(self, "New File", os.path.expanduser('~'),
                                                      "Python Files (*.py)")
        if file_path is not '':
            tab = FIdleTabWidget(parent=self.ui.documents_tabWidget, filepath=file_path)
            tab.editor_changed.connect(self.update_tab_title)
            idx = self.ui.documents_tabWidget.addTab(tab, tab.filename)
            self.ui.documents_tabWidget.setCurrentIndex(idx)

    def save_file(self):
        tab = self._get_current_tab()
        if tab.filepath is None:
            self.save_file_as()
        else:
            with open(tab.filepath, 'w') as fp:
                fp.write(tab.editor.text())
            tab.saved = True

    def save_file_as(self):
        tab = self._get_current_tab()
        path = tab.basepath or os.path.join(os.path.expanduser('~'), tab.filename)
        file_path = QtGui.QFileDialog.getSaveFileName(self, "Save File", path, "Python Files (*.py)")
        if file_path is not '':
            with open(file_path, 'w') as fp:
                fp.write(tab.editor.text())
            tab.filepath = file_path
            tab.saved = True

    def print_file(self):
        pass

    def close_current_tab(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        self.close_tab(idx)

    def close_all_tabs(self):
        print(self.ui.documents_tabWidget.count())
        for i in range(self.ui.documents_tabWidget.count()):
            self.close_tab(0)

    def exit_app(self):
        self.close()

    def show_help_pane(self):
        if self.ui.helpBrowser.url().path() == 'blank':
            src = QtCore.QUrl('http://{0}:{1}/'.format(self.pyconsole_server.host, CONSOLE_HELP_PORT))
            self.ui.helpBrowser.setUrl(src)
        self.ui.helpPane.show()

    def update_tab_title(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        tabname = tab.filename if tab.saved else tab.filename + ' *'
        self.ui.documents_tabWidget.setTabText(idx, tabname)

    def handle_tab_change(self, idx):
        if self.ui.run_remember_checkBox.checkState():
            # don't update run command if checked
            return

        # no tab selected has index of -1
        if idx >= 0:
            tab = self.ui.documents_tabWidget.widget(idx)
            # set the run script command
            command = 'python {0}'.format(self._elide_filepath(tab.filepath))
            self.ui.runScript_command.setText(command)
            self.ui.runScript_command.setToolTip(tab.filepath)
            # set the run script path
            self.runscript_path = tab.filepath
        else:
            self.ui.runScript_command.setText('')
            self.runscript_path = None

    def handle_run_remember(self, state):
        if not state:
            # un-checked
            tab = self._get_current_tab()
            if tab:
                # set the run script command
                command = 'python {0}'.format(tab.filename)
                self.ui.runScript_command.setText(command)
            else:
                self.ui.runScript_command.setText('')

    def close_tab(self, idx):
        # removing the tab doesn't get the widget, so we need to get that first
        widget = self.ui.documents_tabWidget.widget(idx)
        self.ui.documents_tabWidget.removeTab(idx)
        # then delete it
        del widget

    def send_pyconsole_command(self):
        command = self.pyconsole_input.text()
        self.pyconsole_client.send(command)
        self.ui.pyConsole_output.insertPlainText('{0} {1}\n'.format(self.ui.pyConsole_prompt.text(), command))
        self.pyconsole_input.setText("")

    def run_current_script(self):
        # Start a second console that serves the pydoc help
        self.run_console = PyConsoleClient(self.pyconsole_server.host, self.pyconsole_server.port)
        self.run_console.data_ready.connect(lambda x: print(x))
        self.run_console.start()
        # Poll the server until the connection is up and running and then run the script
        timeout = 100
        while True:
            if self.pyconsole_help.send('import pydoc'):
                break
            else:
                time.sleep(0.1)
                timeout -= 1
                if timeout < 0:
                    raise RuntimeError('Could not start the help server!')

    def load_anchor(self, url):
        scheme = url.scheme()
        ret = False
        if scheme == 'help':
            query = dict(url.queryItems())  # queryItems returns list of tuples
            if self.pyconsole_pyversion[0] == 2:
                if query['object'] in py2_exceptions:
                    src = QtCore.QUrl('http://{0}:{1}/exceptions.html#{2}'.format(self.pyconsole_server.host,
                                                                                  CONSOLE_HELP_PORT,
                                                                                  query['object']))
            elif self.pyconsole_pyversion[0] == 3:
                if query['object'] in py3_exceptions:
                    src = QtCore.QUrl('http://{0}:{1}/exceptions.html#{2}'.format(self.pyconsole_server.host,
                                                                                  CONSOLE_HELP_PORT,
                                                                                  query['object']))
            else:
                src = QtCore.QUrl('http://{0}:{1}/exceptions.html'.format(self.pyconsole_server.host,
                                                                                  CONSOLE_HELP_PORT))
            self.ui.helpBrowser.setUrl(src)
            self.ui.helpSearch.setText(urllib.parse.unquote_plus(query['text']))
            self.ui.helpPane.show()
            ret = True
        elif scheme == 'http' or scheme == 'https':
            ret = QtGui.QDesktopServices.openUrl(url)

        if not ret:
            message_box = QtGui.QMessageBox()
            message_box.setText("Cannot open link.")
            message_box.setInformativeText('The link at {0} cannot be opened.'.format(url.path()))
            ok_btn = message_box.addButton(QtGui.QMessageBox.Ok)
            message_box.setDefaultButton(ok_btn)
            message_box.exec_()

    def run_web_search(self):
        query = self.ui.helpSearch.text()
        url = HELP_GOOGLE_URL.format(query=urllib.parse.quote_plus(query))
        qurl = QtCore.QUrl(url)
        QtGui.QDesktopServices.openUrl(qurl)

    def _get_current_tab(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        return tab

    def _process_traceback(self):
        processed_lines = []
        # Process the Traceback buffer
        for line in self.pyconsole_traceback:
            if 'error' in line.lower():
                error = line.split(':')[0].strip()
                link = '<a href="help://?object={0}&text={1}">{2}</a>\n'.format(error,
                                                                                urllib.parse.quote_plus(line),
                                                                                line.strip())
                processed_lines.append(link)
            else:
                processed_lines.append(html.escape(line))
        self.ui.pyConsole_output.moveCursor(QtGui.QTextCursor.End)
        self.ui.pyConsole_output.insertHtml('<pre>{0}</pre></br>'.format(''.join(processed_lines)))
        # Reset Traceback buffer
        self.pyconsole_traceback = []

    def _process_console_stdout(self, line):
        self.ui.pyConsole_output.moveCursor(QtGui.QTextCursor.End)
        words = line.split(' ')
        #print(words)
        # Check for InteractiveConsole prompt
        if len(words) == 2:
            if words[0] == CONSOLE_PS2.strip():
                self.ui.pyConsole_prompt.setText(CONSOLE_PS2)
            elif words[0] == CONSOLE_PS1.strip():
                self.ui.pyConsole_prompt.setText(CONSOLE_PS1)
                if len(self.pyconsole_traceback) > 0:
                    self._process_traceback()
            elif len(self.pyconsole_traceback) > 0:
                self.pyconsole_traceback.append(line)
            else:
                self.ui.pyConsole_output.insertPlainText(line)
        elif words[0].lower() == 'traceback' or len(self.pyconsole_traceback) > 0:
            # Load the Traceback buffer
            self.pyconsole_traceback.append(line)
        else:
            self.ui.pyConsole_output.insertPlainText(line)

        self.ui.pyConsole_output.ensureCursorVisible()

        # Get the version of Python running on the console
        if self.pyconsole_pyversion is None:
            banner = self.ui.pyConsole_output.toPlainText().split('\n')[0]
            regex = re.compile('.*?(\\d)(\\.)(\\d)(\\.)(\\d)', re.IGNORECASE|re.DOTALL)
            match = regex.search(banner)
            if match:
                self.pyconsole_pyversion = (int(match.group(1)), int(match.group(3)), int(match.group(5)))

    def _process_runscript_stdout(self, line):
        words = line.split(' ')
        # print(words)
        # Check for InteractiveConsole prompt
        if len(words) == 2:
            if words[0] == CONSOLE_PS2.strip():
                self.ui.pyConsole_prompt.setText(CONSOLE_PS2)
            elif words[0] == CONSOLE_PS1.strip():
                self.ui.pyConsole_prompt.setText(CONSOLE_PS1)
                if len(self.pyconsole_traceback) > 0:
                    self._process_traceback()
            else:
                self.ui.runScript_output.insertPlainText(line)
        elif words[0].lower() == 'traceback' or len(self.runscript_traceback) > 0:
            # Load the Traceback buffer
            self.runscript_traceback.append(line)
        else:
            self.ui.runScript_output.insertPlainText(line)

        self.ui.runScript_output.ensureCursorVisible()

    def _elide_filepath(self, path):
        basepath, filename = os.path.split(path)
        if len(basepath) > 20:
            return '{0}...{1}{sep}{2}'.format(basepath[:5], basepath[-5:], filename, sep=os.sep)
        else:
            return path