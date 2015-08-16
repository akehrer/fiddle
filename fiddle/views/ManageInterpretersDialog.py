# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManageInterpretersDialog.ui'
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

class Ui_manageInterpreters_Dialog(object):
    def setupUi(self, manageInterpreters_Dialog):
        manageInterpreters_Dialog.setObjectName(_fromUtf8("manageInterpreters_Dialog"))
        manageInterpreters_Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        manageInterpreters_Dialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(manageInterpreters_Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.defaulInterpreter_layout = QtGui.QHBoxLayout()
        self.defaulInterpreter_layout.setObjectName(_fromUtf8("defaulInterpreter_layout"))
        self.defaulInterpreter_label = QtGui.QLabel(manageInterpreters_Dialog)
        self.defaulInterpreter_label.setMinimumSize(QtCore.QSize(18, 18))
        self.defaulInterpreter_label.setMaximumSize(QtCore.QSize(18, 18))
        self.defaulInterpreter_label.setText(_fromUtf8(""))
        self.defaulInterpreter_label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/python_twosnakes.png")))
        self.defaulInterpreter_label.setScaledContents(True)
        self.defaulInterpreter_label.setObjectName(_fromUtf8("defaulInterpreter_label"))
        self.defaulInterpreter_layout.addWidget(self.defaulInterpreter_label)
        self.defaultInterpreterPath_label = QtGui.QLabel(manageInterpreters_Dialog)
        self.defaultInterpreterPath_label.setObjectName(_fromUtf8("defaultInterpreterPath_label"))
        self.defaulInterpreter_layout.addWidget(self.defaultInterpreterPath_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.defaulInterpreter_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.defaulInterpreter_layout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(manageInterpreters_Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.addInterpreter_Button = QtGui.QToolButton(manageInterpreters_Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addInterpreter_Button.setIcon(icon)
        self.addInterpreter_Button.setAutoRaise(True)
        self.addInterpreter_Button.setObjectName(_fromUtf8("addInterpreter_Button"))
        self.horizontalLayout.addWidget(self.addInterpreter_Button)
        self.removeInterpreter_Button = QtGui.QToolButton(manageInterpreters_Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeInterpreter_Button.setIcon(icon1)
        self.removeInterpreter_Button.setAutoRaise(True)
        self.removeInterpreter_Button.setObjectName(_fromUtf8("removeInterpreter_Button"))
        self.horizontalLayout.addWidget(self.removeInterpreter_Button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pyInterpreters_List = QtGui.QListWidget(manageInterpreters_Dialog)
        self.pyInterpreters_List.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.pyInterpreters_List.setProperty("showDropIndicator", False)
        self.pyInterpreters_List.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.pyInterpreters_List.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.pyInterpreters_List.setAlternatingRowColors(True)
        self.pyInterpreters_List.setObjectName(_fromUtf8("pyInterpreters_List"))
        self.verticalLayout.addWidget(self.pyInterpreters_List)
        self.buttonBox = QtGui.QDialogButtonBox(manageInterpreters_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(manageInterpreters_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), manageInterpreters_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), manageInterpreters_Dialog.reject)
        QtCore.QObject.connect(self.addInterpreter_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), manageInterpreters_Dialog.add_interpreter)
        QtCore.QObject.connect(self.removeInterpreter_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), manageInterpreters_Dialog.remove_interpreter)
        QtCore.QMetaObject.connectSlotsByName(manageInterpreters_Dialog)

    def retranslateUi(self, manageInterpreters_Dialog):
        manageInterpreters_Dialog.setWindowTitle(_translate("manageInterpreters_Dialog", "Manage Interpreters", None))
        self.defaultInterpreterPath_label.setText(_translate("manageInterpreters_Dialog", "/", None))
        self.label.setText(_translate("manageInterpreters_Dialog", "User Interpreters", None))
        self.addInterpreter_Button.setText(_translate("manageInterpreters_Dialog", "Add Interpreter", None))
        self.removeInterpreter_Button.setText(_translate("manageInterpreters_Dialog", "Remove Interpreter", None))
        self.pyInterpreters_List.setSortingEnabled(False)

from . import resources_rc
