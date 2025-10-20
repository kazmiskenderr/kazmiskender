# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_ReportsWindow(object):
    def setupUi(self, ReportsWindow):
        ReportsWindow.setObjectName("ReportsWindow")
        ReportsWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(ReportsWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.reportsList = QtWidgets.QListWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.reportsList)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.runReportButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.runReportButton)
        self.exportExcelButton = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLayout.addWidget(self.exportExcelButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        ReportsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ReportsWindow)
        ReportsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ReportsWindow)
        ReportsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ReportsWindow)
        QtCore.QMetaObject.connectSlotsByName(ReportsWindow)

    def retranslateUi(self, ReportsWindow):
        _translate = QtCore.QCoreApplication.translate
        ReportsWindow.setWindowTitle(_translate("ReportsWindow", "Reports"))
        self.runReportButton.setText(_translate("ReportsWindow", "Run Report"))
        self.exportExcelButton.setText(_translate("ReportsWindow", "Export Excel"))
