# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_InventoryWindow(object):
    def setupUi(self, InventoryWindow):
        InventoryWindow.setObjectName("InventoryWindow")
        InventoryWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(InventoryWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.inventoryTable = QtWidgets.QTableView(self.centralwidget)
        self.verticalLayout.addWidget(self.inventoryTable)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.addButton)
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        InventoryWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InventoryWindow)
        InventoryWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InventoryWindow)
        InventoryWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InventoryWindow)
        QtCore.QMetaObject.connectSlotsByName(InventoryWindow)

    def retranslateUi(self, InventoryWindow):
        _translate = QtCore.QCoreApplication.translate
        InventoryWindow.setWindowTitle(_translate("InventoryWindow", "Inventory"))
        self.addButton.setText(_translate("InventoryWindow", "Add"))
        self.editButton.setText(_translate("InventoryWindow", "Edit"))
        self.deleteButton.setText(_translate("InventoryWindow", "Delete"))
