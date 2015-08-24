# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

# Import standard library modules
import logging
import urllib.parse

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import application modules
from fiddle import __version__
from fiddle.views.MainWindow import Ui_MainWindow
from fiddle.controllers.FiddleTabWidget import FiddleTabWidget
from fiddle.controllers.PyConsole import PyConsoleLineEdit, PyConsoleLineCombo
from fiddle.controllers.ManageInterpretersDialog import ManageInterpretersDialog
from fiddle.config import *
from fiddle.helpers.builtins import *

# Set up the logger
logger = logging.getLogger(__name__)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, app=None, files=None):
        super(MainWindow, self).__init__()

        self.app = app

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(WINDOW_TITLE)

        # Initialize actions
        self.init_actions()

        # Initialize statusbar
        self.lbl_pyversion = None
        self.lbl_current_position = None
        self.lbl_encoding = None
        self.init_statusbar()

        # Hide the help pane
        self.ui.helpPane.hide()

        # Hide the Find/Replace frame
        self.ui.findPane.hide()

        # Initialize interpreters
        self.current_interpreter = CONSOLE_PYTHON
        self.current_interpreter_dir = CONSOLE_PYTHON_DIR
        self.interpreters = []
        self.init_interpreters()

        # Initialize Python console
        self.pyconsole_input = PyConsoleLineEdit()
        self.pyconsole_input.returnPressed.connect(self.send_pyconsole_command)
        self.ui.pyconsole_prompt_layout.insertWidget(1, self.pyconsole_input)
        self.ui.pyConsole_output.anchorClicked.connect(self.load_anchor)
        self.pyconsole_process = None
        self.help_process = None
        self.pyconsole_pyversion = None  # stores a tuple of the system Python's version
        self.start_pyconsole_process()
        self.start_pyconsole_help()

        # Console text formats
        self.base_format = None
        self.error_format = None
        self.info_format = None
        self.init_console_text_formats()

        # Initialize run script console
        self.ui.runScript_output.anchorClicked.connect(self.load_anchor)
        self.runscript_process = None
        self.runscript_tab = None

        # Initialize the search providers
        self.search_url = ''
        self.init_search_providers()

        # Initialize recent files
        self.recent_files = []
        self.init_open_recent()

        # Load any files/dirs passed on the command line
        self.init_load_files(files)

    def stop(self):
        try:
            self.pyconsole_process.kill()
            self.pyconsole_process.close()
        except AttributeError:
            pass

        try:
            self.help_process.kill()
            self.help_process.close()
        except AttributeError:
            pass

        try:
            self.runscript_process.kill()
            self.runscript_process.close()
        except AttributeError:
            pass

    def init_load_files(self, paths):
        """
        Given a list of paths, open all the files found. If a path is a directory then open all the files in that
        directory.

        :param list paths:
        :return:
        """
        if paths is not None and len(paths) > 0:
            # Open all the files
            for path in paths:
                if os.path.isfile(path):
                    self.open_filepath(path)
                elif os.path.isdir(path):
                    for item in os.listdir(path):
                        ipath = os.path.join(path, item)
                        if os.path.isfile(ipath):
                            self.open_filepath(ipath)
        else:
            # Add a blank file
            self.new_file()

    def init_actions(self):
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
        self.ui.actionCut.triggered.connect(self.edit_cut)
        self.ui.actionCopy.triggered.connect(self.edit_copy)
        self.ui.actionPaste.triggered.connect(self.edit_paste)
        self.ui.actionSelect_All.triggered.connect(self.edit_select_all)
        self.ui.actionFind.triggered.connect(self.find_in_file)
        self.ui.actionFind_and_Replace.triggered.connect(self.replace_in_file)

        # View actions
        self.ui.actionWord_Wrap.triggered.connect(self.set_editors_wordwrap)
        self.ui.actionShow_Whitespace.triggered.connect(self.set_editors_whitespace)
        self.ui.actionShow_End_of_Line.triggered.connect(self.set_editors_eolchars)

        # Code actions
        self.ui.actionClean_Code.triggered.connect(self.clean_current_editor)
        self.ui.actionCheck_Code.triggered.connect(self.check_current_editor)

        # Console actions
        self.ui.actionShow_Console.triggered.connect(self.toggle_console)
        self.ui.actionRestart_Console.triggered.connect(self.restart_pyconsole_process)
        self.ui.actionHalt_Python_Console.triggered.connect(self.terminate_pyconsole_process)
        self.ui.actionRun_Current_Script.triggered.connect(self.run_current_script)
        self.ui.actionHalt_Current_Script.triggered.connect(self.terminate_current_script)

        # Help actions
        self.ui.actionShow_Help_Pane.triggered.connect(self.toggle_help_pane)
        self.ui.actionAbout_fIDDEL.triggered.connect(self.show_about_fiddle)
        #self.ui.actionFIDDLE_Help.triggered.connect()  # TODO: Create

    def init_search_providers(self):
        ag = QtGui.QActionGroup(self)
        ag.setExclusive(True)
        for item in HELP_WEB_SEARCH_SOURCES:
            a = QtGui.QAction(self)
            a.setData(item)
            a.setText(item['name'])
            a.setCheckable(True)
            a.triggered.connect(self.set_search_provider)
            ag.addAction(a)
            self.ui.menuSearch_Provider.addAction(a)
            if item['name'] == HELP_WEB_SEARCH_SOURCES[0]['name']:
                a.trigger()

    def init_interpreters(self):
        self.ui.menuPython_Interpreter.clear()
        # Add the default actions
        a_manage = QtGui.QAction(self)
        a_manage.setText(self.tr('Manage Interpreters'))
        a_manage.triggered.connect(self.show_manage_interpreters)
        self.ui.menuPython_Interpreter.addAction(a_manage)
        self.ui.menuPython_Interpreter.addSeparator()
        # Add the available interpreters
        ag = QtGui.QActionGroup(self)
        ag.setExclusive(True)
        # Set default interpreter
        a = QtGui.QAction(self)
        a.setData(CONSOLE_PYTHON)
        if PLATFORM == 'win32':
            a.setText(self.tr('(Default) {0}'.format(os.path.dirname(CONSOLE_PYTHON))))
        else:
            a.setText(self.tr('(Default) {0}'.format(CONSOLE_PYTHON)))
        a.setCheckable(True)
        a.setChecked(True)
        a.triggered.connect(self.set_current_interpreter)
        ag.addAction(a)
        self.ui.menuPython_Interpreter.addAction(a)
        # Add additional interpreters
        for item in CONSOLE_PYTHON_INTERPRETERS:
            a = QtGui.QAction(self)
            a.setData(item)
            if item['virtualenv']:
                a.setText(self._elide_filepath(os.path.dirname(item['path']), threshold=50, margin=10))
            else:
                if PLATFORM == 'win32':
                    a.setText(os.path.dirname(item['path']))
                else:
                    a.setText(item['path'])
            a.setCheckable(True)
            a.triggered.connect(self.set_current_interpreter)
            ag.addAction(a)
            self.ui.menuPython_Interpreter.addAction(a)

    def init_open_recent(self):
        if os.path.exists('.recent'):
            with open('.recent') as fp:
                self.recent_files = fp.readlines()
        self.create_recent_files_menu()

    def init_console_text_formats(self):
        # Base format (defined in Qt Designer)
        self.base_format = self.ui.pyConsole_output.currentCharFormat()
        self.base_format.setForeground(QtGui.QColor(CONSOLE_COLOR_BASE))

        # Error format for data on stderr
        self.error_format = QtGui.QTextCharFormat(self.base_format)
        self.error_format.setForeground(QtGui.QColor(CONSOLE_COLOR_ERROR))

        # Info format for data
        self.info_format = QtGui.QTextCharFormat(self.base_format)
        self.info_format.setForeground(QtGui.QColor(CONSOLE_COLOR_INFO))

    def init_statusbar(self):
        # Statusbar
        # you can't add widgets to status bar in Qt Designer, so do it here
        self.lbl_pyversion = QtGui.QLabel()
        self.lbl_pyversion.setMargin(5)
        self.ui.statusbar.addPermanentWidget(self.lbl_pyversion)
        self.lbl_pyversion.setText("")

        self.lbl_encoding = QtGui.QLabel()
        self.lbl_encoding.setMargin(5)
        self.lbl_encoding.setToolTip(self.tr('File encoding'))
        self.ui.statusbar.insertPermanentWidget(0, self.lbl_encoding)
        self.lbl_encoding.setText('UTF-8')

        self.lbl_current_position = QtGui.QLabel()
        self.lbl_current_position.setMargin(5)
        self.lbl_current_position.setToolTip(self.tr('Line no.:Column no.'))
        self.ui.statusbar.insertPermanentWidget(0, self.lbl_current_position)
        self.lbl_current_position.setText('0:0')

    def set_current_interpreter(self):
        action = self.sender()
        item = action.data()
        if os.path.exists(item['path']):
            self.current_interpreter = os.path.normpath(item['path'])
            self.current_interpreter_dir = os.path.dirname(self.current_interpreter)
            self.restart_pyconsole_process()
            self.restart_pyconsole_help()
            idx = self.ui.documents_tabWidget.currentIndex()
            self.handle_tab_change(idx)
        else:
            self.ui.statusbar.showMessage(self.tr('No Python executable at {0}').format(item['path']), 5000)

    def start_pyconsole_process(self):
        # Create a shell process
        self.pyconsole_process = QtCore.QProcess(self)
        self.pyconsole_process.setWorkingDirectory(self.current_interpreter_dir)
        self.pyconsole_process.readyReadStandardError.connect(self.process_console_stderr)
        self.pyconsole_process.readyReadStandardOutput.connect(self.process_console_stdout)
        self.pyconsole_process.finished.connect(self.process_console_finished)
        # Clear any version information
        self.pyconsole_pyversion = None
        # Start the interactive console
        self.pyconsole_process.start(self.current_interpreter,  ['-i'])  # -i makes sure InteractiveConsole is started

    def restart_pyconsole_process(self):
        if self.pyconsole_process is not None:
            self.app.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.print_data_to_pyconsole('\n', self.info_format)
            self.print_data_to_pyconsole(self.tr('Python console is restarting...'), self.info_format)
            self.ui.pyConsole_output.repaint()  # Force message to show
            self.pyconsole_process.terminate()
            if not self.pyconsole_process.waitForFinished(2000):
                self.pyconsole_process.kill()
            self.pyconsole_process.close()
        self.ui.pyConsole_output.clear()
        self.start_pyconsole_process()
        self.app.restoreOverrideCursor()

    def terminate_pyconsole_process(self):
        if self.pyconsole_process is not None:
            self.app.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.print_data_to_pyconsole('\n', self.info_format)
            self.print_data_to_pyconsole(self.tr('Python console is teminating...'), self.info_format)
            self.ui.pyConsole_output.repaint()  # Force message to show
            self.pyconsole_process.terminate()
            if not self.pyconsole_process.waitForFinished(5000):
                self.pyconsole_process.kill()
            self.pyconsole_process.close()
            self.app.restoreOverrideCursor()

    def start_pyconsole_help(self):
        # Create a shell process
        self.help_process = QtCore.QProcess(self)
        # Start the pydoc help server
        self.help_process.setWorkingDirectory(self.current_interpreter_dir)
        self.help_process.start(self.current_interpreter, ['-m', 'pydoc', '-p', str(CONSOLE_HELP_PORT)])
        self.help_process.readyReadStandardError.connect(self.process_help_stderr)
        self.help_process.readyReadStandardOutput.connect(self.process_help_stdout)
        self.help_process.finished.connect(self.process_help_finished)
        # Load the main page in the help pane
        src = QtCore.QUrl('http://{0}:{1}/'.format(CONSOLE_HOST, CONSOLE_HELP_PORT))
        self.ui.helpBrowser.setUrl(src)

    def restart_pyconsole_help(self):
        if self.help_process is not None:
            self.app.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.print_data_to_runconsole('\n', self.info_format)
            self.print_data_to_runconsole(self.tr('Python help is restarting...'), self.info_format)
            self.ui.runScript_output.repaint()  # Force message to show
            self.help_process.terminate()
            if not self.help_process.waitForFinished(2000):
                self.help_process.kill()
            self.help_process.close()
        self.ui.runScript_output.clear()
        self.start_pyconsole_help()
        self.app.restoreOverrideCursor()

    def run_current_script(self):
        # Show the run tab
        self.ui.console_tabWidget.show()
        self.ui.console_tabWidget.setCurrentIndex(1)
        # Clear the output
        self.ui.runScript_output.clear()
        # Create a shell process
        self.runscript_process = QtCore.QProcess(self)
        self.runscript_process.setWorkingDirectory(self.runscript_tab.basepath)
        self.runscript_process.readyReadStandardError.connect(self.process_runscript_stderr)
        self.runscript_process.readyReadStandardOutput.connect(self.process_runscript_stdout)
        self.runscript_process.finished.connect(self.process_runscript_finished)
        # Run the script in the process
        if not os.path.isfile(self.runscript_tab.filepath) or not self.runscript_tab.saved:
            self.runscript_tab.save()
            self.set_current_run_command(self.runscript_tab)  # Update the command to the saved location
        command = self.ui.runScript_command.text()
        self.runscript_process.start(command)

    def terminate_current_script(self):
        if self.runscript_process is not None:
            self.print_data_to_runconsole('\n', self.info_format)
            self.print_data_to_runconsole(self.tr('Script is terminating...'), self.info_format)
            self.ui.runScript_output.repaint()  # Force message to show
            self.app.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.runscript_process.terminate()
            if not self.runscript_process.waitForFinished(2000):
                self.runscript_process.kill()
            self.app.restoreOverrideCursor()

    def create_tab(self, filepath=None):
        tab = FiddleTabWidget(parent=self.ui.documents_tabWidget, filepath=filepath)
        tab.editor_changed.connect(self.update_tab_title)
        tab.cursor_changed.connect(self.update_cursor_position)
        return tab

    def new_file(self):
        tab = self.create_tab()
        tabname = tab.filename if tab.saved else tab.filename + ' *'
        idx = self.ui.documents_tabWidget.addTab(tab, tabname)
        self.ui.documents_tabWidget.setCurrentIndex(idx)

    def open_file(self):
        tab = self.ui.documents_tabWidget.currentWidget()
        filepath = QtGui.QFileDialog.getOpenFileName(None,
                                                     None,
                                                     os.path.expanduser('~') if tab is None else tab.basepath,
                                                     ';;'.join(FILE_TYPES))
        if filepath != '':
            self.open_filepath(filepath)
            self.update_recent_files(filepath)

    def open_filepath(self, filepath):
        if not os.path.exists(filepath):
            self.ui.statusbar.showMessage(self.tr('No file at {0}').format(filepath), 5000)
            return None

        if filepath is not '' and not None:
            tab = self.create_tab(filepath)
            if os.path.normcase(CONSOLE_PYTHON_DIR) in os.path.normcase(filepath):
                # Give users a hint they may be editing a system file by changing background color
                tab.editor.lexer.setPaper(QtGui.QColor(EDITOR_CARET_LINE_COLOR))
            idx = self.ui.documents_tabWidget.addTab(tab, tab.filename)
            self.ui.documents_tabWidget.setCurrentIndex(idx)
            self.ui.documents_tabWidget.setTabToolTip(idx, filepath)
            return tab
        else:
            return None

    def open_recent_filepath(self):
        action = self.sender()
        if action:
            self.open_filepath(action.data())

    def update_recent_files(self, filepath):
        """
        Save file path to recent files, truncating to 10 files and removing duplicates.

        :param str filepath:
        :return:
        """
        try:
            self.recent_files.append(filepath)
        except AttributeError:
            self.recent_files = []
            self.recent_files.append(filepath)
        # Remove duplicates
        seen = []
        filtered = []
        for item in self.recent_files:
            if item in seen:
                continue
            seen.append(item)
            filtered.append(item)
        with open('.recent', 'w') as fp:
            if len(filtered) > 10:
                fp.write('\n'.join(filtered[-10:]))
            else:
                fp.write('\n'.join(filtered))
        self.create_recent_files_menu()

    def create_recent_files_menu(self):
        self.ui.menuOpen_Recent.clear()
        for filepath in reversed(self.recent_files):
            sfp = filepath.strip()
            if sfp != '':
                a = QtGui.QAction(self.ui.menuOpen_Recent)
                a.setText(self._elide_filepath(sfp, threshold=50, margin=10))
                a.setData(sfp)
                a.triggered.connect(self.open_recent_filepath)
                self.ui.menuOpen_Recent.addAction(a)

    def save_file(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        tab.save()
        self.ui.documents_tabWidget.setTabToolTip(idx, tab.filepath)
        self.handle_tab_change(idx)

    def save_file_as(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        tab.save_as()
        self.ui.documents_tabWidget.setTabToolTip(idx, tab.filepath)
        self.handle_tab_change(idx)

    def print_file(self):
        pass

    def exit_app(self):
        self.close()

    def edit_cut(self):
        try:
            cw = self.app.focusWidget()
            cw.cut()
        except AttributeError:
            pass

    def edit_copy(self):
        try:
            cw = self.app.focusWidget()
            cw.copy()
        except AttributeError:
            pass

    def edit_paste(self):
        try:
            cw = self.app.focusWidget()
            cw.paste()
        except AttributeError:
            pass

    def edit_select_all(self):
        try:
            cw = self.app.focusWidget()
            cw.selectAll()
        except AttributeError:
            pass

    def close_current_tab(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        self.close_tab(idx)

    def close_all_tabs(self):
        for i in range(self.ui.documents_tabWidget.count()):
            self.close_tab(0)

    def close_tab(self, idx):
        # removing the tab doesn't get the widget, so we need to get that first...
        widget = self.ui.documents_tabWidget.widget(idx)
        self.ui.documents_tabWidget.removeTab(idx)
        # ...then delete it
        del widget

    def set_editors_wordwrap(self, state):
        """
        Set the display of the word wrap in all the editors.

        :param bool state:
        :return:

        See QsiScinitilla.setWrapMode()
        """
        for i in range(self.ui.documents_tabWidget.count()):
            tab = self.ui.documents_tabWidget.widget(i)
            tab.editor.wordwrap = state

    def set_editors_whitespace(self, state):
        """
        Set the display of the whitespace characters in all the editors.

        :param bool state:
        :return:

        See QsiScinitilla.setEolVisibility()
        """
        for i in range(self.ui.documents_tabWidget.count()):
            tab = self.ui.documents_tabWidget.widget(i)
            tab.editor.whitespace = state

    def set_editors_eolchars(self, state):
        """
        Set the display of the end-of-line characters in all the editors

        :param bool state:
        :return:

        See QsiScinitilla.setWhitespaceVisibility()
        """
        for i in range(self.ui.documents_tabWidget.count()):
            tab = self.ui.documents_tabWidget.widget(i)
            tab.editor.eolchars = state

    def clean_current_editor(self):
        """
        Run the `clean_code` function in the currenly displayed editor widget.

        :return:
        """
        self.app.setOverrideCursor(QtCore.Qt.WaitCursor)
        tab = self.ui.documents_tabWidget.currentWidget()
        tab.editor.clean_code()
        self.app.restoreOverrideCursor()

    def check_current_editor(self):
        """
        Run the `check_code` function in the currently displayed editor widget.

        :return:
        """
        self.app.setOverrideCursor(QtCore.Qt.WaitCursor)
        tab = self.ui.documents_tabWidget.currentWidget()
        tab.editor.check_code(tab.filepath)
        self.app.restoreOverrideCursor()

    def toggle_help_pane(self):
        if self.ui.helpBrowser.url().path() == 'blank':
            src = QtCore.QUrl('http://{0}:{1}/'.format(self.pyconsole_server.host, CONSOLE_HELP_PORT))
            self.ui.helpBrowser.setUrl(src)
        if self.ui.helpPane.isVisible():
            self.ui.helpPane.hide()
        else:
            self.ui.helpPane.show()
            self.ui.helpSearch.selectAll()
            self.ui.helpSearch.setFocus()

    def toggle_console(self):
        if self.ui.consolePane.isHidden():
            self.ui.consolePane.show()
        else:
            self.ui.consolePane.hide()

    def set_search_provider(self):
        action = self.sender()
        data = action.data()
        self.search_url = data['query_tmpl']
        self.ui.searchProvider_label.setText(data['name'])

    def show_about_fiddle(self):
        message_box = QtGui.QMessageBox()
        message_box.setWindowTitle(self.tr('About fIDDLE'))
        message_box.setText('fIDDLE {0}'.format(__version__))
        message_box.setInformativeText(ABOUT_FIDDLE)
        ok_btn = message_box.addButton(QtGui.QMessageBox.Ok)
        message_box.setDefaultButton(ok_btn)
        message_box.exec_()

    def show_manage_interpreters(self):
        """
        Display the Manage Interpreters dialog and save any changes if the Save button in clicked.

        :return:
        """
        dialog = ManageInterpretersDialog(self)
        ret = dialog.exec_()
        if ret == QtGui.QDialog.Accepted:
            with open('interpreters.json', 'w') as fp:
                CONSOLE_PYTHON_INTERPRETERS = dialog.temp_interpreters
                json.dump(CONSOLE_PYTHON_INTERPRETERS, fp)
            self.init_interpreters()

    def find_in_file(self):
        if self.ui.findPane.isHidden():
            self.ui.findPane.show()
            
        self.ui.find_text_lineEdit.setFocus()
        self.ui.find_text_lineEdit.selectAll()

        if self.ui.find_text_lineEdit.text() != '':
            current_doc = self.ui.documents_tabWidget.currentWidget()
            if current_doc is not None:
                current_doc.find_text(self.ui.find_text_lineEdit.text(),
                                      self.ui.find_re_checkBox.isChecked(),
                                      self.ui.find_case_checkBox.isChecked(),
                                      self.ui.find_word_checkBox.isChecked(),
                                      True,  # Always wrap
                                      self.ui.find_selection_checkBox.isChecked())

    def find_in_file_previous(self):
        if self.ui.find_text_lineEdit.text() != '':
            current_doc = self.ui.documents_tabWidget.currentWidget()
            if current_doc is not None:
                current_doc.find_text(self.ui.find_text_lineEdit.text(),
                                      self.ui.find_re_checkBox.isChecked(),
                                      self.ui.find_case_checkBox.isChecked(),
                                      self.ui.find_word_checkBox.isChecked(),
                                      True,  # Always wrap
                                      self.ui.find_selection_checkBox.isChecked(),
                                      forward=False)

    def replace_in_file(self):
        if self.ui.findPane.isHidden():
            self.ui.findPane.show()
            self.ui.find_text_lineEdit.setFocus()

        if self.ui.replace_text_lineEdit.text() != '':
            current_doc = self.ui.documents_tabWidget.currentWidget()
            if current_doc is not None:
                current_doc.replace_text(self.ui.find_text_lineEdit.text(),
                                         self.ui.replace_text_lineEdit.text(),
                                         self.ui.find_re_checkBox.isChecked(),
                                         self.ui.find_case_checkBox.isChecked(),
                                         self.ui.find_word_checkBox.isChecked(),
                                         True,  # Always wrap
                                         self.ui.find_selection_checkBox.isChecked())

    def replace_all_in_file(self):
        if self.ui.replace_text_lineEdit.text() != '':
            current_doc = self.ui.documents_tabWidget.currentWidget()
            if current_doc is not None:
                i = current_doc.replace_all_text(self.ui.find_text_lineEdit.text(),
                                                 self.ui.replace_text_lineEdit.text(),
                                                 self.ui.find_re_checkBox.isChecked(),
                                                 self.ui.find_case_checkBox.isChecked(),
                                                 self.ui.find_word_checkBox.isChecked(),
                                                 self.ui.find_selection_checkBox.isChecked())
                self.ui.statusbar.showMessage(self.tr('Replaced {0} instances').format(i), 5000)

    def update_tab_title(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        tabname = tab.filename if tab.saved else tab.filename + ' *'
        self.ui.documents_tabWidget.setTabText(idx, tabname)

    def update_cursor_position(self, line, idx):
        """
        Process cursor position changes from editors for display in statusbar.

        :param int line:
        :param int idx:
        :return:
        """
        self.lbl_current_position.setText('{0}:{1}'.format(line+1, idx+1))  # zero indexed

    def set_current_run_command(self, tab):
        # set the run script command
        if PLATFORM == 'win32':
            command = '{0} "{1}" '.format(self.current_interpreter, tab.filepath)
        else:
            command = '{0} {1} '.format(self.current_interpreter, tab.filepath)
        self.ui.runScript_command.setText(command)
        self.ui.runScript_command.setToolTip(command)
        self.runscript_tab = tab

    def handle_tab_change(self, idx):
        if idx >= 0:
            tab = self.ui.documents_tabWidget.widget(idx)
            self.lbl_encoding.setText('{0}'.format(tab.encoding.upper()
                                                   if 'utf' or 'ascii' in tab.encoding.lower()
                                                   else tab.encoding))

            if self.ui.run_remember_checkBox.checkState():
                # don't update run command if checked
                return
            else:
                self.set_current_run_command(tab)
        else:
            self.ui.runScript_command.setText('')
            self.runscript_tab = None

    def handle_run_remember(self, chk_state):
        if not chk_state:
            tab = self.ui.documents_tabWidget.currentWidget()
            if tab:
                # set the run script command
                if PLATFORM == 'win32':
                    command = '{0} "{1}" '.format(self.current_interpreter, tab.filepath)
                else:
                    command = '{0} {1} '.format(self.current_interpreter, tab.filepath)
                self.ui.runScript_command.setText(command)
                self.ui.runScript_command.setToolTip(command)
            else:
                self.ui.runScript_command.setText('')

    def send_pyconsole_command(self):
        command = self.pyconsole_input.text()
        self.pyconsole_process.write('{0}\n'.format(command))
        cursor = self.ui.pyConsole_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText('{0}{1}'.format(command, os.linesep))
        self.ui.pyConsole_output.ensureCursorVisible()
        self.pyconsole_input.setText("")

    def load_anchor(self, url):
        """
        This slot processes URLs for specific actions internal to the application or loads the URLs in the system
        web browser.

        :param QtCore.QUrl url:
            The URL to process, it may have schemes beyond http(s)
        :return bool:
            Whether the function handled the signal or not

        URLs may have schemes beyond http(s) that the application recognizes and processes for display by the
        built-in browser widget.  They follow the standard format {scheme}://{query} where query is a standard URL
        query (?item1=var1&item2=var2)
        Schemes:
        - help: load current interpreter's documentation for a specific Python object, often used to link to error
                documentation in the console tracebacks
            - Query items:
                - object: the Python object to get docstring
                - text: the full text that caused the link to the object (often an error), this is loaded in to the
                        help search line widget
        - goto: load a file in to an editor tab and move the cursor to the beginning of a specific line, often used to
                show the user where in a file and error was raised in the console tracebacks
            - Query items:
                - filepath: the full path to the file to load
                - linenum: the line number to move the cursor to
        - http(s): load the full URL in the system browser
        """
        scheme = url.scheme()
        ret = False
        if scheme == 'help':
            query = dict(url.queryItems())  # queryItems returns list of tuples
            src = QtCore.QUrl('http://{0}:{1}/'.format(CONSOLE_HOST,
                                                       CONSOLE_HELP_PORT))
            if self.pyconsole_pyversion[0] == 2:
                if query['object'] in py2_exceptions:
                    src = QtCore.QUrl('http://{0}:{1}/exceptions.html#{2}'.format(CONSOLE_HOST,
                                                                                  CONSOLE_HELP_PORT,
                                                                                  query['object']))
            elif self.pyconsole_pyversion[0] == 3:
                if query['object'] in py3_exceptions:
                    src = QtCore.QUrl('http://{0}:{1}/builtins.html#{2}'.format(CONSOLE_HOST,
                                                                                CONSOLE_HELP_PORT,
                                                                                query['object']))
            try:
                self.ui.helpBrowser.setUrl(src)
                self.ui.helpSearch.setText(urllib.parse.unquote_plus(query['text']))
                self.ui.helpPane.show()
                ret = True
            except UnboundLocalError:
                ret = False
        elif scheme == 'goto':
            query = dict(url.queryItems())  # queryItems returns list of tuples
            filepath = urllib.parse.unquote_plus(query['filepath'])
            linenum = int(query['linenum']) - 1
            found = False
            # Is the file already open?
            for i in range(self.ui.documents_tabWidget.count()):
                tab = self.ui.documents_tabWidget.widget(i)
                # Take care of slash discrepancies, ahem Windows
                if os.path.normcase(tab.filepath) == os.path.normcase(filepath):
                    self.ui.documents_tabWidget.setCurrentWidget(tab)
                    tab.editor.setCursorPosition(linenum, 0)
                    tab.editor.ensureLineVisible(linenum)
                    tab.editor.setFocus()
                    found = True
                    break
            if not found:
                # Load the offending file in another editor
                try:
                    tab = self.open_filepath(filepath)
                    tab.editor.setCursorPosition(linenum, 0)
                    tab.editor.ensureLineVisible(linenum)
                    tab.editor.setFocus()
                except AttributeError:
                    message_box = QtGui.QMessageBox()
                    message_box.setWindowTitle(self.tr('File Error'))
                    message_box.setText(self.tr('Cannot open file'))
                    message_box.setInformativeText(self.tr('The file at {0} cannot be opened.').format(filepath))
                    ok_btn = message_box.addButton(QtGui.QMessageBox.Ok)
                    message_box.setDefaultButton(ok_btn)
                    message_box.exec_()
            ret = True
        elif scheme == 'http' or scheme == 'https':
            # Open URL in system browser
            ret = QtGui.QDesktopServices.openUrl(url)

        if not ret:
            message_box = QtGui.QMessageBox()
            message_box.setWindowTitle(self.tr('Link Error'))
            message_box.setText(self.tr('Cannot open link'))
            message_box.setInformativeText(self.tr('The link at {0} cannot be opened.').format(url.path()))
            ok_btn = message_box.addButton(QtGui.QMessageBox.Ok)
            message_box.setDefaultButton(ok_btn)
            message_box.exec_()

    def run_web_search(self):
        """
        Combine the search text from the search input with the current web search template and open it with the system
        browser.

        :return:
        """
        query = self.ui.helpSearch.text()
        url = self.search_url.format(query=urllib.parse.quote_plus(query))
        qurl = QtCore.QUrl(url)
        QtGui.QDesktopServices.openUrl(qurl)

    def print_data_to_pyconsole(self, data, fmt, html=False):
        cursor = self.ui.pyConsole_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        if html:
            cursor.insertHtml(data)
        else:
            cursor.insertText(data, fmt)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.pyConsole_output.ensureCursorVisible()

    def print_data_to_runconsole(self, data, fmt, html=False):
        cursor = self.ui.runScript_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        if html:
            cursor.insertHtml(data)
        else:
            cursor.insertText(data, fmt)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.runScript_output.ensureCursorVisible()

    def process_stderr_lines(self, lines, cursor):
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
                try:
                    i = line.split(':')
                    error = i[0]
                    desc = os.linesep.join(i[1:])
                    link = '<a href="help://?object={0}&text={1}">{2}</a>'.format(error,
                                                                                  urllib.parse.quote_plus(ls),
                                                                                  error)
                    cursor.insertHtml(link)
                    cursor.insertText(':{0}'.format(desc), self.error_format)
                    cursor.insertText(os.linesep, self.base_format)
                except ValueError:
                    cursor.insertText(line, self.error_format)
            elif 'file' in lsl:
                m = CONSOLE_RE_LINENUM.search(line)
                if m:
                    groups = m.groups()
                    filepath = groups[1]
                    linenum = groups[3]
                    module = groups[5]
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
                self.ui.pyConsole_prompt.setText(CONSOLE_PS1)
                cursor.insertText(ls + ' ', self.base_format)
            elif CONSOLE_PS2 in line:
                self.ui.pyConsole_prompt.setText(CONSOLE_PS2)
                cursor.insertText(ls + ' ', self.base_format)
            else:
                cursor.insertText(line, self.error_format)

    def process_console_stdout(self):
        self.pyconsole_process.setReadChannel(QtCore.QProcess.StandardOutput)
        data = self.pyconsole_process.readAll()
        lines = data.data().decode().split(os.linesep)
        for line in lines:
            line = line + os.linesep  # Line separators were stripped off in the split, add them back
            # Create clickable links
            m = CONSOLE_RE_HTTP.findall(line)
            if m:
                linked = line
                for g in m:
                    linked = linked.replace(g, '<a href={0}>{0}</a>'.format(g))
                self.print_data_to_pyconsole(linked, self.base_format, html=True)
                self.print_data_to_pyconsole(os.linesep, self.base_format)
            else:
                self.print_data_to_pyconsole(line, self.base_format)

    def process_console_stderr(self):
        self.pyconsole_process.setReadChannel(QtCore.QProcess.StandardError)
        data = self.pyconsole_process.readAll()
        lines = data.data().decode().split(os.linesep)
        cursor = self.ui.pyConsole_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.process_stderr_lines(lines, cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.pyConsole_output.ensureCursorVisible()

        # Get the version of Python running on the console
        if self.pyconsole_pyversion is None:
            banner = self.ui.pyConsole_output.toPlainText().split(os.linesep)[0]
            match = CONSOLE_RE_PYVER.search(banner)
            if match:
                self.pyconsole_pyversion = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
                self.lbl_pyversion.setText('Python {0}.{1}.{2}'.format(*self.pyconsole_pyversion))

    def process_console_finished(self, code):
        self.ui.pyConsole_output.insertPlainText(os.linesep)
        self.ui.pyConsole_output.insertPlainText(self.tr('Exited with code {0}').format(code))
        self.ui.runScript_output.ensureCursorVisible()
        self.pyconsole_process.close()

    def process_runscript_stdout(self):
        self.runscript_process.setReadChannel(QtCore.QProcess.StandardOutput)
        data = self.runscript_process.readAll()
        lines = data.data().decode().split(os.linesep)
        for line in lines:
            line = line + os.linesep  # Line separators were stripped off in the split, add them back
            m = CONSOLE_RE_HTTP.findall(line)
            if m:
                linked = line
                for g in m:
                    linked = linked.replace(g, '<a href={0}>{0}</a>'.format(g))
                self.print_data_to_runconsole(linked, self.base_format, html=True)
                self.print_data_to_runconsole(os.linesep, self.base_format)
            else:
                self.print_data_to_runconsole(line, self.base_format)

    def process_runscript_stderr(self):
        self.runscript_process.setReadChannel(QtCore.QProcess.StandardError)
        data = self.runscript_process.readAll()
        lines = data.data().decode().split(os.linesep)
        cursor = self.ui.runScript_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.process_stderr_lines(lines, cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.runScript_output.ensureCursorVisible()

    def process_runscript_finished(self, code):
        self.print_data_to_runconsole(os.linesep, self.info_format)
        self.print_data_to_runconsole(self.tr('Exited with code {0}').format(code), self.info_format)
        self.runscript_process.close()

    def process_help_stdout(self):
        self.help_process.setReadChannel(QtCore.QProcess.StandardOutput)
        data = self.help_process.readAll()
        cursor = self.ui.runScript_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(data.data().decode(), self.info_format)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.runScript_output.ensureCursorVisible()

    def process_help_stderr(self):
        self.help_process.setReadChannel(QtCore.QProcess.StandardError)
        data = self.help_process.readAll()
        lines = data.data().decode().split(os.linesep)
        cursor = self.ui.runScript_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.process_stderr_lines(lines, cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.runScript_output.ensureCursorVisible()

    def process_help_finished(self, code):
        cursor = self.ui.runScript_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(os.linesep, self.info_format)
        cursor.insertText(self.tr('HELP: Exited with code {0}').format(code), self.info_format)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.runScript_output.ensureCursorVisible()
        self.help_process.close()

    @staticmethod
    def _elide_filepath(path, threshold=20, margin=5):
        """
        Shorten a file path string using '...' for easier display
        :param str path:
            The file path to shorten
        :param int threshold:
            Paths with lengths less than then will not be shortened
        :param int margin:
            This many characters will be kept before and after the '...'
        :return str:
        """
        basepath, filename = os.path.split(path)
        if len(basepath) > threshold:
            return '{0}...{1}{sep}{2}'.format(basepath[:margin], basepath[-margin:], filename, sep=os.sep)
        else:
            return path
