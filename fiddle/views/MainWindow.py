# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.resize(1366, 768)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.editor_help_Splitter = QtGui.QSplitter(self.centralwidget)
        self.editor_help_Splitter.setOrientation(QtCore.Qt.Horizontal)
        self.editor_help_Splitter.setChildrenCollapsible(False)
        self.editor_help_Splitter.setObjectName(_fromUtf8("editor_help_Splitter"))
        self.editor_console_Splitter = QtGui.QSplitter(self.editor_help_Splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editor_console_Splitter.sizePolicy().hasHeightForWidth())
        self.editor_console_Splitter.setSizePolicy(sizePolicy)
        self.editor_console_Splitter.setOrientation(QtCore.Qt.Vertical)
        self.editor_console_Splitter.setOpaqueResize(True)
        self.editor_console_Splitter.setChildrenCollapsible(False)
        self.editor_console_Splitter.setObjectName(_fromUtf8("editor_console_Splitter"))
        self.layoutWidget = QtGui.QWidget(self.editor_console_Splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.documents_tabWidget = QtGui.QTabWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.documents_tabWidget.sizePolicy().hasHeightForWidth())
        self.documents_tabWidget.setSizePolicy(sizePolicy)
        self.documents_tabWidget.setMinimumSize(QtCore.QSize(800, 300))
        self.documents_tabWidget.setAutoFillBackground(False)
        self.documents_tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.documents_tabWidget.setElideMode(QtCore.Qt.ElideRight)
        self.documents_tabWidget.setDocumentMode(True)
        self.documents_tabWidget.setTabsClosable(True)
        self.documents_tabWidget.setMovable(True)
        self.documents_tabWidget.setObjectName(_fromUtf8("documents_tabWidget"))
        self.verticalLayout_5.addWidget(self.documents_tabWidget)
        self.findReplace_Frame = QtGui.QFrame(self.layoutWidget)
        self.findReplace_Frame.setEnabled(True)
        self.findReplace_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.findReplace_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.findReplace_Frame.setObjectName(_fromUtf8("findReplace_Frame"))
        self.gridLayout = QtGui.QGridLayout(self.findReplace_Frame)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(5, 1, 5, 1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.find_next_Button = QtGui.QPushButton(self.findReplace_Frame)
        self.find_next_Button.setObjectName(_fromUtf8("find_next_Button"))
        self.gridLayout.addWidget(self.find_next_Button, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.findReplace_Frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.find_text_lineEdit = QtGui.QLineEdit(self.findReplace_Frame)
        self.find_text_lineEdit.setObjectName(_fromUtf8("find_text_lineEdit"))
        self.gridLayout.addWidget(self.find_text_lineEdit, 1, 1, 1, 2)
        self.replace_text_lineEdit = QtGui.QLineEdit(self.findReplace_Frame)
        self.replace_text_lineEdit.setObjectName(_fromUtf8("replace_text_lineEdit"))
        self.gridLayout.addWidget(self.replace_text_lineEdit, 2, 1, 1, 2)
        self.replace_Button = QtGui.QPushButton(self.findReplace_Frame)
        self.replace_Button.setObjectName(_fromUtf8("replace_Button"))
        self.gridLayout.addWidget(self.replace_Button, 2, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.findReplace_Frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.find_previous_Button = QtGui.QPushButton(self.findReplace_Frame)
        self.find_previous_Button.setObjectName(_fromUtf8("find_previous_Button"))
        self.gridLayout.addWidget(self.find_previous_Button, 1, 4, 1, 1)
        self.replace_all_Button = QtGui.QPushButton(self.findReplace_Frame)
        self.replace_all_Button.setObjectName(_fromUtf8("replace_all_Button"))
        self.gridLayout.addWidget(self.replace_all_Button, 2, 4, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.find_re_checkBox = QtGui.QCheckBox(self.findReplace_Frame)
        self.find_re_checkBox.setObjectName(_fromUtf8("find_re_checkBox"))
        self.horizontalLayout_3.addWidget(self.find_re_checkBox)
        self.find_case_checkBox = QtGui.QCheckBox(self.findReplace_Frame)
        self.find_case_checkBox.setObjectName(_fromUtf8("find_case_checkBox"))
        self.horizontalLayout_3.addWidget(self.find_case_checkBox)
        self.find_word_checkBox = QtGui.QCheckBox(self.findReplace_Frame)
        self.find_word_checkBox.setObjectName(_fromUtf8("find_word_checkBox"))
        self.horizontalLayout_3.addWidget(self.find_word_checkBox)
        self.find_selection_checkBox = QtGui.QCheckBox(self.findReplace_Frame)
        self.find_selection_checkBox.setObjectName(_fromUtf8("find_selection_checkBox"))
        self.horizontalLayout_3.addWidget(self.find_selection_checkBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.toolButton_2 = QtGui.QToolButton(self.findReplace_Frame)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.toolButton_2.setFont(font)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.horizontalLayout_3.addWidget(self.toolButton_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 5)
        self.gridLayout.setColumnStretch(1, 2)
        self.verticalLayout_5.addWidget(self.findReplace_Frame)
        self.verticalLayout_5.setStretch(0, 2)
        self.console_tabWidget = QtGui.QTabWidget(self.editor_console_Splitter)
        self.console_tabWidget.setObjectName(_fromUtf8("console_tabWidget"))
        self.pyconsole_Tab = QtGui.QWidget()
        self.pyconsole_Tab.setObjectName(_fromUtf8("pyconsole_Tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pyconsole_Tab)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pyConsole_output = QtGui.QTextBrowser(self.pyconsole_Tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pyConsole_output.setFont(font)
        self.pyConsole_output.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.pyConsole_output.setReadOnly(True)
        self.pyConsole_output.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.pyConsole_output.setOpenExternalLinks(False)
        self.pyConsole_output.setOpenLinks(False)
        self.pyConsole_output.setObjectName(_fromUtf8("pyConsole_output"))
        self.verticalLayout.addWidget(self.pyConsole_output)
        self.pyconsole_prompt_layout = QtGui.QHBoxLayout()
        self.pyconsole_prompt_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.pyconsole_prompt_layout.setSpacing(0)
        self.pyconsole_prompt_layout.setObjectName(_fromUtf8("pyconsole_prompt_layout"))
        self.pyConsole_prompt = QtGui.QLabel(self.pyconsole_Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyConsole_prompt.sizePolicy().hasHeightForWidth())
        self.pyConsole_prompt.setSizePolicy(sizePolicy)
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
        self.pyconsole_restart_Button = QtGui.QToolButton(self.pyconsole_Tab)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/arrow_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pyconsole_restart_Button.setIcon(icon)
        self.pyconsole_restart_Button.setAutoRaise(True)
        self.pyconsole_restart_Button.setObjectName(_fromUtf8("pyconsole_restart_Button"))
        self.pyconsole_prompt_layout.addWidget(self.pyconsole_restart_Button)
        self.pyconsole_halt_Button = QtGui.QToolButton(self.pyconsole_Tab)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/cross.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pyconsole_halt_Button.setIcon(icon1)
        self.pyconsole_halt_Button.setAutoRaise(True)
        self.pyconsole_halt_Button.setObjectName(_fromUtf8("pyconsole_halt_Button"))
        self.pyconsole_prompt_layout.addWidget(self.pyconsole_halt_Button)
        self.verticalLayout.addLayout(self.pyconsole_prompt_layout)
        self.console_tabWidget.addTab(self.pyconsole_Tab, _fromUtf8(""))
        self.runscript_Tab = QtGui.QWidget()
        self.runscript_Tab.setObjectName(_fromUtf8("runscript_Tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.runscript_Tab)
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.runscript_Tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.runScript_command = QtGui.QLineEdit(self.runscript_Tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.runScript_command.setFont(font)
        self.runScript_command.setObjectName(_fromUtf8("runScript_command"))
        self.horizontalLayout.addWidget(self.runScript_command)
        self.run_remember_checkBox = QtGui.QCheckBox(self.runscript_Tab)
        self.run_remember_checkBox.setObjectName(_fromUtf8("run_remember_checkBox"))
        self.horizontalLayout.addWidget(self.run_remember_checkBox)
        self.runScript_button = QtGui.QToolButton(self.runscript_Tab)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/play_green.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.runScript_button.setIcon(icon2)
        self.runScript_button.setAutoRaise(True)
        self.runScript_button.setObjectName(_fromUtf8("runScript_button"))
        self.horizontalLayout.addWidget(self.runScript_button)
        self.toolButton = QtGui.QToolButton(self.runscript_Tab)
        self.toolButton.setIcon(icon1)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.runScript_output = QtGui.QTextBrowser(self.runscript_Tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.runScript_output.setFont(font)
        self.runScript_output.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.runScript_output.setOpenLinks(False)
        self.runScript_output.setObjectName(_fromUtf8("runScript_output"))
        self.verticalLayout_4.addWidget(self.runScript_output)
        self.console_tabWidget.addTab(self.runscript_Tab, _fromUtf8(""))
        self.helpPane = QtGui.QWidget(self.editor_help_Splitter)
        self.helpPane.setObjectName(_fromUtf8("helpPane"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.helpPane)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_5 = QtGui.QLabel(self.helpPane)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.toolButton1 = QtGui.QToolButton(self.helpPane)
        self.toolButton1.setAutoRaise(True)
        self.toolButton1.setObjectName(_fromUtf8("toolButton1"))
        self.horizontalLayout_4.addWidget(self.toolButton1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.helpSearch = QtGui.QLineEdit(self.helpPane)
        self.helpSearch.setObjectName(_fromUtf8("helpSearch"))
        self.horizontalLayout_2.addWidget(self.helpSearch)
        self.web_search_Button = QtGui.QPushButton(self.helpPane)
        self.web_search_Button.setObjectName(_fromUtf8("web_search_Button"))
        self.horizontalLayout_2.addWidget(self.web_search_Button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.label_4 = QtGui.QLabel(self.helpPane)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.helpBrowser = QtWebKit.QWebView(self.helpPane)
        self.helpBrowser.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.helpBrowser.setObjectName(_fromUtf8("helpBrowser"))
        self.verticalLayout_3.addWidget(self.helpBrowser)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_6.addWidget(self.editor_help_Splitter)
        self.verticalLayout_6.setStretch(0, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOpen_Recent = QtGui.QMenu(self.menuFile)
        self.menuOpen_Recent.setObjectName(_fromUtf8("menuOpen_Recent"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuShell = QtGui.QMenu(self.menubar)
        self.menuShell.setObjectName(_fromUtf8("menuShell"))
        self.menuPython_Interpreter = QtGui.QMenu(self.menuShell)
        self.menuPython_Interpreter.setObjectName(_fromUtf8("menuPython_Interpreter"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuSearch_Provider = QtGui.QMenu(self.menuHelp)
        self.menuSearch_Provider.setObjectName(_fromUtf8("menuSearch_Provider"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuShow = QtGui.QMenu(self.menuView)
        self.menuShow.setObjectName(_fromUtf8("menuShow"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.main_toolBar = QtGui.QToolBar(MainWindow)
        self.main_toolBar.setMovable(False)
        self.main_toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.main_toolBar.setIconSize(QtCore.QSize(16, 16))
        self.main_toolBar.setFloatable(False)
        self.main_toolBar.setObjectName(_fromUtf8("main_toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.main_toolBar)
        self.actionNew = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/page_white.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon3)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave_File = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/disk.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_File.setIcon(icon5)
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/cut.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon6)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionCopy = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/page_white_copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon7)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/paste_plain.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon8)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionSelect_All = QtGui.QAction(MainWindow)
        self.actionSelect_All.setObjectName(_fromUtf8("actionSelect_All"))
        self.actionFind = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/find.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind.setIcon(icon9)
        self.actionFind.setObjectName(_fromUtf8("actionFind"))
        self.actionFind_and_Replace = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/find_replace.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind_and_Replace.setIcon(icon10)
        self.actionFind_and_Replace.setObjectName(_fromUtf8("actionFind_and_Replace"))
        self.actionRestart_Console = QtGui.QAction(MainWindow)
        self.actionRestart_Console.setObjectName(_fromUtf8("actionRestart_Console"))
        self.actionFIDDLE_Help = QtGui.QAction(MainWindow)
        self.actionFIDDLE_Help.setObjectName(_fromUtf8("actionFIDDLE_Help"))
        self.actionAbout_fIDDEL = QtGui.QAction(MainWindow)
        self.actionAbout_fIDDEL.setObjectName(_fromUtf8("actionAbout_fIDDEL"))
        self.actionRun_Current_Script = QtGui.QAction(MainWindow)
        self.actionRun_Current_Script.setObjectName(_fromUtf8("actionRun_Current_Script"))
        self.actionShow_Help_Pane = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/help.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Help_Pane.setIcon(icon11)
        self.actionShow_Help_Pane.setObjectName(_fromUtf8("actionShow_Help_Pane"))
        self.actionShow_Console = QtGui.QAction(MainWindow)
        self.actionShow_Console.setObjectName(_fromUtf8("actionShow_Console"))
        self.actionHalt_Python_Console = QtGui.QAction(MainWindow)
        self.actionHalt_Python_Console.setObjectName(_fromUtf8("actionHalt_Python_Console"))
        self.actionHalt_Current_Script = QtGui.QAction(MainWindow)
        self.actionHalt_Current_Script.setObjectName(_fromUtf8("actionHalt_Current_Script"))
        self.actionShow_Whitespace = QtGui.QAction(MainWindow)
        self.actionShow_Whitespace.setCheckable(True)
        self.actionShow_Whitespace.setObjectName(_fromUtf8("actionShow_Whitespace"))
        self.actionShow_End_of_Line = QtGui.QAction(MainWindow)
        self.actionShow_End_of_Line.setCheckable(True)
        self.actionShow_End_of_Line.setObjectName(_fromUtf8("actionShow_End_of_Line"))
        self.actionWord_Wrap = QtGui.QAction(MainWindow)
        self.actionWord_Wrap.setCheckable(True)
        self.actionWord_Wrap.setObjectName(_fromUtf8("actionWord_Wrap"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuOpen_Recent.menuAction())
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addAction(self.actionSave_File_As)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionFind_and_Replace)
        self.menuShell.addAction(self.actionShow_Console)
        self.menuShell.addAction(self.menuPython_Interpreter.menuAction())
        self.menuShell.addSeparator()
        self.menuShell.addAction(self.actionRun_Current_Script)
        self.menuShell.addAction(self.actionHalt_Current_Script)
        self.menuShell.addSeparator()
        self.menuShell.addAction(self.actionRestart_Console)
        self.menuShell.addAction(self.actionHalt_Python_Console)
        self.menuHelp.addAction(self.actionShow_Help_Pane)
        self.menuHelp.addAction(self.menuSearch_Provider.menuAction())
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionFIDDLE_Help)
        self.menuHelp.addAction(self.actionAbout_fIDDEL)
        self.menuShow.addAction(self.actionShow_Whitespace)
        self.menuShow.addAction(self.actionShow_End_of_Line)
        self.menuView.addAction(self.actionClose_Tab)
        self.menuView.addAction(self.actionClose_All_Tabs)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionWord_Wrap)
        self.menuView.addAction(self.menuShow.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuShell.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.main_toolBar.addAction(self.actionNew)
        self.main_toolBar.addAction(self.actionOpen)
        self.main_toolBar.addAction(self.actionSave_File)
        self.main_toolBar.addSeparator()
        self.main_toolBar.addAction(self.actionCut)
        self.main_toolBar.addAction(self.actionCopy)
        self.main_toolBar.addAction(self.actionPaste)
        self.main_toolBar.addSeparator()
        self.main_toolBar.addAction(self.actionFind)
        self.main_toolBar.addAction(self.actionFind_and_Replace)
        self.main_toolBar.addSeparator()
        self.main_toolBar.addAction(self.actionShow_Help_Pane)

        self.retranslateUi(MainWindow)
        self.documents_tabWidget.setCurrentIndex(-1)
        self.console_tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.documents_tabWidget, QtCore.SIGNAL(_fromUtf8("tabCloseRequested(int)")), MainWindow.close_tab)
        QtCore.QObject.connect(self.documents_tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), MainWindow.handle_tab_change)
        QtCore.QObject.connect(self.run_remember_checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), MainWindow.handle_run_remember)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.helpPane.hide)
        QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.findReplace_Frame.hide)
        QtCore.QObject.connect(self.find_next_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.find_in_file)
        QtCore.QObject.connect(self.find_previous_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.find_in_file_previous)
        QtCore.QObject.connect(self.find_text_lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.find_in_file)
        QtCore.QObject.connect(self.replace_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.replace_in_file)
        QtCore.QObject.connect(self.replace_all_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.replace_all_in_file)
        QtCore.QObject.connect(self.helpSearch, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.run_web_search)
        QtCore.QObject.connect(self.pyconsole_restart_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.restart_pyconsole_process)
        QtCore.QObject.connect(self.pyconsole_halt_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.terminate_pyconsole_process)
        QtCore.QObject.connect(self.runScript_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.run_current_script)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.terminate_current_script)
        QtCore.QObject.connect(self.web_search_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.run_web_search)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.find_next_Button.setText(_translate("MainWindow", "Next", None))
        self.label_2.setText(_translate("MainWindow", "Find", None))
        self.replace_Button.setText(_translate("MainWindow", "Replace", None))
        self.label_3.setText(_translate("MainWindow", "Replace", None))
        self.find_previous_Button.setText(_translate("MainWindow", "Previous", None))
        self.replace_all_Button.setText(_translate("MainWindow", "Replace All", None))
        self.find_re_checkBox.setText(_translate("MainWindow", "RegEx", None))
        self.find_case_checkBox.setText(_translate("MainWindow", "Match Case", None))
        self.find_word_checkBox.setText(_translate("MainWindow", "Whole Word", None))
        self.find_selection_checkBox.setText(_translate("MainWindow", "In Selection", None))
        self.toolButton_2.setText(_translate("MainWindow", "X", None))
        self.pyConsole_prompt.setText(_translate("MainWindow", ">>>", None))
        self.pyconsole_restart_Button.setToolTip(_translate("MainWindow", "Restart Python Console", None))
        self.pyconsole_restart_Button.setText(_translate("MainWindow", "...", None))
        self.pyconsole_halt_Button.setToolTip(_translate("MainWindow", "Halt Python Console", None))
        self.pyconsole_halt_Button.setText(_translate("MainWindow", "...", None))
        self.console_tabWidget.setTabText(self.console_tabWidget.indexOf(self.pyconsole_Tab), _translate("MainWindow", "Python Console", None))
        self.label.setText(_translate("MainWindow", "Run Command", None))
        self.run_remember_checkBox.setText(_translate("MainWindow", "Remember", None))
        self.runScript_button.setToolTip(_translate("MainWindow", "Run Script", None))
        self.runScript_button.setText(_translate("MainWindow", "Run", None))
        self.toolButton.setToolTip(_translate("MainWindow", "Halt Running Script", None))
        self.toolButton.setText(_translate("MainWindow", "Halt", None))
        self.console_tabWidget.setTabText(self.console_tabWidget.indexOf(self.runscript_Tab), _translate("MainWindow", "Run Script", None))
        self.label_5.setText(_translate("MainWindow", "Web Search", None))
        self.toolButton1.setToolTip(_translate("MainWindow", "Hide help pane", None))
        self.toolButton1.setText(_translate("MainWindow", "X", None))
        self.web_search_Button.setText(_translate("MainWindow", "Search", None))
        self.label_4.setText(_translate("MainWindow", "Built-in Help", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuOpen_Recent.setTitle(_translate("MainWindow", "Open Recent", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuShell.setTitle(_translate("MainWindow", "Console", None))
        self.menuPython_Interpreter.setTitle(_translate("MainWindow", "Python Interpreter", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuSearch_Provider.setTitle(_translate("MainWindow", "Search Provider", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuShow.setTitle(_translate("MainWindow", "Show", None))
        self.main_toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
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
        self.actionRestart_Console.setText(_translate("MainWindow", "Restart Python Console", None))
        self.actionFIDDLE_Help.setText(_translate("MainWindow", "fIDDLE Help", None))
        self.actionAbout_fIDDEL.setText(_translate("MainWindow", "About fIDDLE", None))
        self.actionRun_Current_Script.setText(_translate("MainWindow", "Run Current Script", None))
        self.actionRun_Current_Script.setShortcut(_translate("MainWindow", "F5", None))
        self.actionShow_Help_Pane.setText(_translate("MainWindow", "Show/Hide Help", None))
        self.actionShow_Help_Pane.setShortcut(_translate("MainWindow", "Ctrl+H", None))
        self.actionShow_Console.setText(_translate("MainWindow", "Show/Hide Console", None))
        self.actionHalt_Python_Console.setText(_translate("MainWindow", "Halt Python Console", None))
        self.actionHalt_Current_Script.setText(_translate("MainWindow", "Halt Current Script", None))
        self.actionShow_Whitespace.setText(_translate("MainWindow", "Show Whitespace", None))
        self.actionShow_End_of_Line.setText(_translate("MainWindow", "Show End of Line", None))
        self.actionWord_Wrap.setText(_translate("MainWindow", "Word Wrap", None))

from PyQt4 import QtWebKit
from . import resources_rc
