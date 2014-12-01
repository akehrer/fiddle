# Import standard library modules
import logging
import os

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import application window view
from fidle.views.MainWindow import Ui_MainWindow
from fidle.controllers.FIdleTabWidget import FIdleTabWidget
from fidle.controllers.FIdlePyConsole import PyConsoleInterpreter, PyConsoleLineEdit
from fidle.config import WINDOW_TITLE

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

        # Initialize Python console
        self.pyconsole_input = PyConsoleLineEdit()
        self.ui.pyconsole_prompt_layout.insertWidget(1, self.pyconsole_input)
        self.pyconsole_input.returnPressed.connect(self.send_pyconsole_command)
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
        self.ui.actionClose_File.triggered.connect(self.close_file)
        self.ui.actionClose_All_Files.triggered.connect(self.close_all_files)

        self.ui.actionExit.triggered.connect(self.exit_app)

        # Edit actions
        # TODO

    def init_open_recent(self):
        pass

    def start_pyconsole(self):
        self.pyconsole = PyConsoleInterpreter()
        self.ui.pyConsole_prompt.setText(self.pyconsole.ps1)
        self.ui.pyConsole_output.insertPlainText(self.pyconsole.banner)

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
        pass

    def save_file_as(self):
        pass

    def print_file(self):
        pass

    def close_file(self):
        pass

    def close_all_files(self):
        pass

    def exit_app(self):
        pass

    def update_tab_title(self):
        idx = self.ui.documents_tabWidget.currentIndex()
        tab = self.ui.documents_tabWidget.widget(idx)
        tabname = tab.filename if tab.saved else tab.filename + ' *'
        self.ui.documents_tabWidget.setTabText(idx, tabname)

    def handle_tab_change(self, idx):
        tab = self.ui.documents_tabWidget.widget(idx)
        # set the run script command
        command = 'python {0}'.format(tab.filename)
        self.ui.runScript_command.setText(command)

    def close_tab(self, idx):
        # removing the tab doesn't get the widget, so we need to get that first
        widget = self.ui.documents_tabWidget.widget(idx)
        self.ui.documents_tabWidget.removeTab(idx)
        # then delete it
        del widget

    def send_pyconsole_command(self):
        command = self.pyconsole_input.text()
        try:
            more, res = self.pyconsole.push(command)
        except EOFError:
            more = False
            res = ''

        self.ui.pyConsole_output.insertPlainText('{0} {1}\n'.format(self.ui.pyConsole_prompt.text(), command))
        if res != '':
            self.ui.pyConsole_output.insertPlainText(res + '\n')

        if more:
            self.ui.pyConsole_prompt.setText(self.pyconsole.ps2)
        else:
            self.ui.pyConsole_prompt.setText(self.pyconsole.ps1)

        self.ui.pyConsole_output.ensureCursorVisible()
        self.pyconsole_input.setText('')