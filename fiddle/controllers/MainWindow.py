# Import standard library modules
import logging
import os
import re
import urllib.parse

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import application modules
from fiddle.views.MainWindow import Ui_MainWindow
from fiddle.controllers.FiddleTabWidget import FIdleTabWidget
from fiddle.controllers.PyConsole import PyConsoleServer, PyConsoleLineEdit
from fiddle.controllers.pyqterm import TerminalWidget
from fiddle.config import WINDOW_TITLE, APP_DIR
from fiddle.utils import find_python_exe

# Set up the logger
logger = logging.getLogger(__name__)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, portable=False):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(WINDOW_TITLE)

        # Initialize actions
        self.init_menu_actions()

        # Hide the help pane
        self.ui.helpPane.hide()

        # Get the Python executable path
        self.python_exe = find_python_exe()

        # Initialize Python console
        self.pyterminal = TerminalWidget()
        self.pyconsole_input = PyConsoleLineEdit()
        self.ui.pyconsole_prompt_layout.insertWidget(1, self.pyconsole_input)
        self.pyconsole_input.returnPressed.connect(self.send_pyconsole_command)
        self.ui.pyConsole_output.anchorClicked.connect(self.load_anchor)
        self.pyconsole = None
        self.start_pyconsole()

        # Add a blank file
        self.new_file()

    def stop(self):
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

    def init_open_recent(self):
        pass

    def start_pyconsole(self):
        console_script = os.path.join(APP_DIR, 'scripts', 'console_server.py')
        self.pyconsole = PyConsoleServer('python', console_script)
        self.pyconsole.start()

        # self.pyconsole.stream_out.new_line.connect(self._process_console_stdout)
        # self.pyconsole.stream_err.new_line.connect(self._process_console_stderr)
        # self.pyconsole.stream_out.start()
        # self.pyconsole.stream_err.start()
        # self.ui.pyConsole_prompt.setText(self.pyconsole.ps1)
        # self.ui.pyConsole_output.insertPlainText(self.pyconsole.read_out(timeout=0.5))

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

    def update_tab_title(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        tabname = tab.filename if tab.saved else tab.filename + ' *'
        self.ui.documents_tabWidget.setTabText(idx, tabname)

    def handle_tab_change(self, idx):
        # no tab selected has index of -1
        if idx >= 0:
            tab = self.ui.documents_tabWidget.widget(idx)
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
        try:
            #more, res, err = self.pyconsole.push(command)
            self.pyconsole.push(command)
            res = '' #self.pyconsole.read_out()
            err = '' #self.pyconsole.read_err()
            more = True
        except EOFError:
            more = False
            res = ''
            err = ''

        self.ui.pyConsole_output.insertPlainText('{0} {1}\n'.format(self.ui.pyConsole_prompt.text(), command))
        if res != '':
            self.ui.pyConsole_output.insertPlainText(res + '\n')
        if err != '':
            # TODO: better process the traceback to provide help
            p_err = self._process_traceback(err)  # comes back as HTML
            self.ui.pyConsole_output.insertHtml('<pre>{0}</pre><br>'.format(p_err))

        if more:
            self.ui.pyConsole_prompt.setText(self.pyconsole.ps2)
        else:
            self.ui.pyConsole_prompt.setText(self.pyconsole.ps1)

        self.ui.pyConsole_output.ensureCursorVisible()
        self.pyconsole_input.setText('')

    def load_anchor(self, url):
        scheme = url.scheme()
        if scheme == 'help':
            query = dict(url.queryItems())  # queryItems returns list of tuples
            cmd = 'help({})'.format(query['object'])
            more, res, err = self.pyconsole.push(cmd)
            self.ui.helpPane.setPlainText(res)
            self.ui.helpPane.show()

    def _get_current_tab(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        return tab

    def _process_traceback(self, trace):
        lines = trace.split('\n')
        processed_lines = []
        for line in lines:
            if 'error' in line.lower():
                error = line.split(':')[0].strip()
                link = '<a href="help://?object={0}&text={1}">{2}</a>'.format(error, urllib.parse.quote_plus(line), line)
                processed_lines.append(link)
            else:
                processed_lines.append(line)
        return '\n'.join(processed_lines)

    def _process_console_stdout(self, line):
        print(line.split(' '))
        # print('Out: ' + line.__repr__())

    def _process_console_stderr(self, line):
        print('Err: ' + line.__repr__())
