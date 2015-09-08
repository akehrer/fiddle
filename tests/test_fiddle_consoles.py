# Copyright (c) 2015 Aaron Kehrer
# Licensed under the terms of the MIT License
# (see fiddle/__init__.py for details)

import os
import unittest
from string import ascii_letters, digits, punctuation

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from tests import FiddleTestFixture
from tests.helpers import *


class FiddleConsolesTest(FiddleTestFixture):
    def test_no_console_restart(self):
        """
        Can the program handle trying to restart the Python console interpreter when one doesn't exist?
        :return:
        """
        old_int = self.form.current_interpreter
        old_int_dir = self.form.current_interpreter_dir
        self.form.current_interpreter = ''
        self.form.current_interpreter_dir = ''
        self.form.restart_pyconsole_process()
        self.assertEqual('', self.form.pyconsole_output.toPlainText())
        self.form.current_interpreter = old_int
        self.form.current_interpreter_dir = old_int_dir

    def test_no_help_restart(self):
        """
        Can the program handle trying to restart the help interpreter when one doesn't exist?
        :return:
        """
        old_int = self.form.current_interpreter
        old_int_dir = self.form.current_interpreter_dir
        self.form.current_interpreter = ''
        self.form.current_interpreter_dir = ''
        self.form.restart_pyconsole_help()
        self.assertEqual('', self.form.ui.helpBrowser.page().mainFrame().toPlainText())
        self.form.current_interpreter = old_int
        self.form.current_interpreter_dir = old_int_dir

    def test_pyconsole_insert_ascii(self):
        """
        Can ASCII text be sent to the Python console from the input widget?
        :return:
        """
        self.form.pyconsole_output.clear()
        console_pre_txt = self.form.pyconsole_output.toPlainText()
        test_str = ascii_letters + digits + punctuation
        QTest.keyClicks(self.form.pyconsole_output, "i = '{0}'".format(test_str))
        QTest.keyClick(self.form.pyconsole_output, Qt.Key_Return)

        console_post_txt = self.form.pyconsole_output.toPlainText()
        self.assertNotEqual(console_pre_txt, console_post_txt)
        self.assertTrue(test_str in console_post_txt)

    def test_pyconsole_history(self):
        """
        Is there a history of commands send to the Python console that can be cycled through?
        :return:
        """
        test_strs = [ascii_letters, digits, punctuation]
        # Load the history
        for ts in test_strs:
            QTest.keyClicks(self.form.pyconsole_output, "i = '{0}'".format(ts), delay=50)
            QTest.keyClick(self.form.pyconsole_output, Qt.Key_Return, delay=200)

    def test_console_NameError_link(self):
        """
        Does causing a NameError on the Python console result in a help//: link
        :return:
        """
        self.form.pyconsole_output.clear()
        console_pre_txt = self.form.pyconsole_output.toPlainText()
        QTest.keyClick(self.form.pyconsole_output, Qt.Key_I, delay=100)
        QTest.keyClick(self.form.pyconsole_output, Qt.Key_Return, delay=200)
        console_post_txt = self.form.pyconsole_output.toPlainText()
        console_post_html = self.form.pyconsole_output.toHtml()
        self.assertNotEqual(console_pre_txt, console_post_txt)
        self.assertTrue('href="help://?object=NameError' in console_post_html)

    def test_runscript_command_default_interpreter(self):
        """
        Does the run script command contain the current interpreter and tab script path?
        :return:
        """
        tab = self.form.ui.documents_tabWidget.currentWidget()
        cmd = self.form.ui.runScript_command.text()
        self.assertIn(self.form.current_interpreter, cmd)
        self.assertIn(tab.filepath, cmd)

    def test_runscript_command_openfile(self):
        """
        Does opening a new .py file change the run script command?
        :return:
        """
        tab1 = self.form.ui.documents_tabWidget.currentWidget()
        cmd1 = self.form.ui.runScript_command.text()
        self.assertIn(tab1.filepath, cmd1)
        # Load file
        srcpath = os.path.join(self.data_dir, 'server.py')
        self.form.open_filepath(srcpath)
        tab2 = self.form.ui.documents_tabWidget.currentWidget()
        cmd2 = self.form.ui.runScript_command.text()
        self.assertIn(tab2.filepath, cmd2)
        self.assertNotEqual(cmd1, cmd2)

    def test_runscript_command_change_tab(self):
        """
        Does changing the tab change the run script command?
        :return:
        """
        tab1 = self.form.ui.documents_tabWidget.currentWidget()
        cmd1 = self.form.ui.runScript_command.text()
        self.assertIn(tab1.filepath, cmd1)
        # Load file
        srcpath = os.path.join(self.data_dir, 'server.py')
        self.form.open_filepath(srcpath)
        tab2 = self.form.ui.documents_tabWidget.currentWidget()
        cmd2 = self.form.ui.runScript_command.text()
        self.assertIn(tab2.filepath, cmd2)
        # Change tab
        self.form.ui.documents_tabWidget.setCurrentWidget(tab1)
        cmd3 = self.form.ui.runScript_command.text()
        self.assertIn(tab1.filepath, cmd3)
        self.assertNotEqual(cmd1, cmd2)
        self.assertEqual(cmd1, cmd3)

    def test_halt_python_console(self):
        """
        Can the Python console be cleanly halted?
        :return:
        """
        self.form.terminate_pyconsole_process()
        self.assertEqual(self.form.pyconsole_process.state(), 0)

    def test_halt_help(self):
        """
        Can the Python help be cleanly halted?
        :return:
        """
        self.form.terminate_pyconsole_help()
        self.assertEqual(self.form.help_process.state(), 0)

    def test_halt_running_script(self):
        """
        Can a long running script be cleanly halted?
        :return:
        """
        srcpath = os.path.join(self.data_dir, 'run_forever.py')
        self.form.open_filepath(srcpath)
        cmd = self.form.ui.runScript_command.text()
        self.assertIn('run_forever.py', cmd)
        self.form.ui.actionRun_Current_Script.trigger()
        self.assertGreater(self.form.runscript_process.state(), 0)
        QTest.qWait(200)
        self.form.terminate_current_script()
        self.assertEqual(self.form.runscript_process.state(), 0)


if __name__ == "__main__":
    unittest.main()