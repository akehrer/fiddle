# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Tue Dec  2 10:57:54 2014
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 768)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.editorHelp_splitter = QtGui.QSplitter(self.centralwidget)
        self.editorHelp_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.editorHelp_splitter.setObjectName(_fromUtf8("editorHelp_splitter"))
        self.editorConsole_splitter = QtGui.QSplitter(self.editorHelp_splitter)
        self.editorConsole_splitter.setOrientation(QtCore.Qt.Vertical)
        self.editorConsole_splitter.setObjectName(_fromUtf8("editorConsole_splitter"))
        self.documents_tabWidget = QtGui.QTabWidget(self.editorConsole_splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.documents_tabWidget.sizePolicy().hasHeightForWidth())
        self.documents_tabWidget.setSizePolicy(sizePolicy)
        self.documents_tabWidget.setAutoFillBackground(False)
        self.documents_tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.documents_tabWidget.setElideMode(QtCore.Qt.ElideRight)
        self.documents_tabWidget.setDocumentMode(True)
        self.documents_tabWidget.setTabsClosable(True)
        self.documents_tabWidget.setMovable(True)
        self.documents_tabWidget.setObjectName(_fromUtf8("documents_tabWidget"))
        self.tabWidget = QtGui.QTabWidget(self.editorConsole_splitter)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pyConsole_output = QtGui.QTextBrowser(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pyConsole_output.setFont(font)
        self.pyConsole_output.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.pyConsole_output.setReadOnly(True)
        self.pyConsole_output.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.pyConsole_output.setOpenExternalLinks(False)
        self.pyConsole_output.setOpenLinks(False)
        self.pyConsole_output.setObjectName(_fromUtf8("pyConsole_output"))
        self.verticalLayout.addWidget(self.pyConsole_output)
        self.pyconsole_prompt_layout = QtGui.QHBoxLayout()
        self.pyconsole_prompt_layout.setSpacing(0)
        self.pyconsole_prompt_layout.setObjectName(_fromUtf8("pyconsole_prompt_layout"))
        self.pyConsole_prompt = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pyConsole_prompt.setFont(font)
        self.pyConsole_prompt.setStyleSheet(_fromUtf8("background-color: white;"))
        self.pyConsole_prompt.setFrameShape(QtGui.QFrame.NoFrame)
        self.pyConsole_prompt.setFrameShadow(QtGui.QFrame.Plain)
        self.pyConsole_prompt.setTextFormat(QtCore.Qt.PlainText)
        self.pyConsole_prompt.setObjectName(_fromUtf8("pyConsole_prompt"))
        self.pyconsole_prompt_layout.addWidget(self.pyConsole_prompt)
        self.verticalLayout.addLayout(self.pyconsole_prompt_layout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.runScript_command = QtGui.QLineEdit(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.runScript_command.setFont(font)
        self.runScript_command.setObjectName(_fromUtf8("runScript_command"))
        self.horizontalLayout.addWidget(self.runScript_command)
        self.runScript_button = QtGui.QPushButton(self.tab_2)
        self.runScript_button.setObjectName(_fromUtf8("runScript_button"))
        self.horizontalLayout.addWidget(self.runScript_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.runScript_output = QtGui.QPlainTextEdit(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.runScript_output.setFont(font)
        self.runScript_output.setReadOnly(True)
        self.runScript_output.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.runScript_output.setObjectName(_fromUtf8("runScript_output"))
        self.verticalLayout_4.addWidget(self.runScript_output)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.helpPane = QtGui.QTextEdit(self.editorHelp_splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpPane.sizePolicy().hasHeightForWidth())
        self.helpPane.setSizePolicy(sizePolicy)
        self.helpPane.setReadOnly(True)
        self.helpPane.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.helpPane.setObjectName(_fromUtf8("helpPane"))
        self.verticalLayout_3.addWidget(self.editorHelp_splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuShell = QtGui.QMenu(self.menubar)
        self.menuShell.setObjectName(_fromUtf8("menuShell"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpen_Recent = QtGui.QAction(MainWindow)
        self.actionOpen_Recent.setObjectName(_fromUtf8("actionOpen_Recent"))
        self.actionSave_File = QtGui.QAction(MainWindow)
        self.actionSave_File.setObjectName(_fromUtf8("actionSave_File"))
        self.actionSave_File_As = QtGui.QAction(MainWindow)
        self.actionSave_File_As.setObjectName(_fromUtf8("actionSave_File_As"))
        self.actionPrint = QtGui.QAction(MainWindow)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionClose_Tab = QtGui.QAction(MainWindow)
        self.actionClose_Tab.setObjectName(_fromUtf8("actionClose_Tab"))
        self.actionClose_All_Tabs = QtGui.QAction(MainWindow)
        self.actionClose_All_Tabs.setObjectName(_fromUtf8("actionClose_All_Tabs"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionSelect_All = QtGui.QAction(MainWindow)
        self.actionSelect_All.setObjectName(_fromUtf8("actionSelect_All"))
        self.actionFind = QtGui.QAction(MainWindow)
        self.actionFind.setObjectName(_fromUtf8("actionFind"))
        self.actionFind_and_Replace = QtGui.QAction(MainWindow)
        self.actionFind_and_Replace.setObjectName(_fromUtf8("actionFind_and_Replace"))
        self.actionRestart = QtGui.QAction(MainWindow)
        self.actionRestart.setObjectName(_fromUtf8("actionRestart"))
        self.actionFIDLE_Help = QtGui.QAction(MainWindow)
        self.actionFIDLE_Help.setObjectName(_fromUtf8("actionFIDLE_Help"))
        self.actionPython_Help = QtGui.QAction(MainWindow)
        self.actionPython_Help.setObjectName(_fromUtf8("actionPython_Help"))
        self.actionAbout_fIDEL = QtGui.QAction(MainWindow)
        self.actionAbout_fIDEL.setObjectName(_fromUtf8("actionAbout_fIDEL"))
        self.actionRun_Current_Script = QtGui.QAction(MainWindow)
        self.actionRun_Current_Script.setObjectName(_fromUtf8("actionRun_Current_Script"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpen_Recent)
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addAction(self.actionSave_File_As)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionClose_Tab)
        self.menuFile.addAction(self.actionClose_All_Tabs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionFind_and_Replace)
        self.menuShell.addAction(self.actionRun_Current_Script)
        self.menuShell.addAction(self.actionRestart)
        self.menuHelp.addAction(self.actionFIDLE_Help)
        self.menuHelp.addAction(self.actionPython_Help)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_fIDEL)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuShell.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.documents_tabWidget.setCurrentIndex(-1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.documents_tabWidget, QtCore.SIGNAL(_fromUtf8("tabCloseRequested(int)")), MainWindow.close_tab)
        QtCore.QObject.connect(self.documents_tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), MainWindow.handle_tab_change)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pyConsole_prompt.setText(_translate("MainWindow", ">>>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Python Console", None))
        self.label.setText(_translate("MainWindow", "Run Command", None))
        self.runScript_button.setText(_translate("MainWindow", "Run", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Run Script", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuShell.setTitle(_translate("MainWindow", "Run", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent", None))
        self.actionSave_File.setText(_translate("MainWindow", "Save File", None))
        self.actionSave_File.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionSave_File_As.setText(_translate("MainWindow", "Save File As", None))
        self.actionPrint.setText(_translate("MainWindow", "Print", None))
        self.actionPrint.setShortcut(_translate("MainWindow", "Ctrl+P", None))
        self.actionClose_Tab.setText(_translate("MainWindow", "Close Tab", None))
        self.actionClose_All_Tabs.setText(_translate("MainWindow", "Close All Tabs", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionCut.setText(_translate("MainWindow", "Cut", None))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X", None))
        self.actionCopy.setText(_translate("MainWindow", "Copy", None))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C", None))
        self.actionPaste.setText(_translate("MainWindow", "Paste", None))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V", None))
        self.actionSelect_All.setText(_translate("MainWindow", "Select All", None))
        self.actionSelect_All.setShortcut(_translate("MainWindow", "Ctrl+A", None))
        self.actionFind.setText(_translate("MainWindow", "Find", None))
        self.actionFind.setShortcut(_translate("MainWindow", "Ctrl+F", None))
        self.actionFind_and_Replace.setText(_translate("MainWindow", "Find and Replace", None))
        self.actionFind_and_Replace.setShortcut(_translate("MainWindow", "Ctrl+R", None))
        self.actionRestart.setText(_translate("MainWindow", "Restart Python Console", None))
        self.actionFIDLE_Help.setText(_translate("MainWindow", "fIDLE Help", None))
        self.actionPython_Help.setText(_translate("MainWindow", "Python Help", None))
        self.actionAbout_fIDEL.setText(_translate("MainWindow", "About fIDLE", None))
        self.actionRun_Current_Script.setText(_translate("MainWindow", "Run Current Script", None))
        self.actionRun_Current_Script.setShortcut(_translate("MainWindow", "F5", None))

