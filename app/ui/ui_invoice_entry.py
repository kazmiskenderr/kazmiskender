# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_InvoiceWindow(object):
    def setupUi(self, InvoiceWindow):
        InvoiceWindow.setObjectName("InvoiceWindow")
        InvoiceWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(InvoiceWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.customerCombo = QtWidgets.QComboBox(self.centralwidget)
        self.verticalLayout.addWidget(self.customerCombo)
        self.invoiceTable = QtWidgets.QTableView(self.centralwidget)
        self.verticalLayout.addWidget(self.invoiceTable)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.addLineButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.addLineButton)
        self.removeLineButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.removeLineButton)
        self.saveInvoiceButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.saveInvoiceButton)
        self.exportPdfButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.exportPdfButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        InvoiceWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InvoiceWindow)
        InvoiceWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InvoiceWindow)
        InvoiceWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InvoiceWindow)
        QtCore.QMetaObject.connectSlotsByName(InvoiceWindow)

    def retranslateUi(self, InvoiceWindow):
        _translate = QtCore.QCoreApplication.translate
        InvoiceWindow.setWindowTitle(_translate("InvoiceWindow", "Invoices"))
        self.addLineButton.setText(_translate("InvoiceWindow", "Add Line"))
        self.removeLineButton.setText(_translate("InvoiceWindow", "Remove Line"))
        self.saveInvoiceButton.setText(_translate("InvoiceWindow", "Save Invoice"))
        self.exportPdfButton.setText(_translate("InvoiceWindow", "Export PDF"))
