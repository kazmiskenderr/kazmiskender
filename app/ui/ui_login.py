# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(300, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginDialog)
        self.usernameEdit = QtWidgets.QLineEdit(LoginDialog)
        self.verticalLayout.addWidget(self.usernameEdit)
        self.passwordEdit = QtWidgets.QLineEdit(LoginDialog)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout.addWidget(self.passwordEdit)
        self.errorLabel = QtWidgets.QLabel(LoginDialog)
        self.verticalLayout.addWidget(self.errorLabel)
        self.loginButton = QtWidgets.QPushButton(LoginDialog)
        self.verticalLayout.addWidget(self.loginButton)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Login"))
        self.usernameEdit.setPlaceholderText(_translate("LoginDialog", "Username"))
        self.passwordEdit.setPlaceholderText(_translate("LoginDialog", "Password"))
        self.errorLabel.setText("")
        self.loginButton.setText(_translate("LoginDialog", "Login"))
