# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.inventoryButton = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.inventoryButton)
        self.purchasingButton = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.purchasingButton)
        self.invoicingButton = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.invoicingButton)
        self.reportsButton = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.reportsButton)
        self.logoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.logoutButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Warehouse Management"))
        self.inventoryButton.setText(_translate("MainWindow", "Inventory"))
        self.purchasingButton.setText(_translate("MainWindow", "Purchasing"))
        self.invoicingButton.setText(_translate("MainWindow", "Invoicing"))
        self.reportsButton.setText(_translate("MainWindow", "Reports"))
        self.logoutButton.setText(_translate("MainWindow", "Log out"))
