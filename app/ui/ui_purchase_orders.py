# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_PurchaseWindow(object):
    def setupUi(self, PurchaseWindow):
        PurchaseWindow.setObjectName("PurchaseWindow")
        PurchaseWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(PurchaseWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.ordersTable = QtWidgets.QTableView(self.centralwidget)
        self.verticalLayout.addWidget(self.ordersTable)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.newOrderButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.newOrderButton)
        self.receiveButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.receiveButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        PurchaseWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PurchaseWindow)
        PurchaseWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PurchaseWindow)
        PurchaseWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PurchaseWindow)
        QtCore.QMetaObject.connectSlotsByName(PurchaseWindow)

    def retranslateUi(self, PurchaseWindow):
        _translate = QtCore.QCoreApplication.translate
        PurchaseWindow.setWindowTitle(_translate("PurchaseWindow", "Purchase Orders"))
        self.newOrderButton.setText(_translate("PurchaseWindow", "New Order"))
        self.receiveButton.setText(_translate("PurchaseWindow", "Mark as Received"))
        self.cancelButton.setText(_translate("PurchaseWindow", "Cancel Order"))
