"""PySide6 windows wiring business logic to repositories."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PySide6 import QtCore, QtGui, QtWidgets

from app.database import SessionLocal
from app.repository.unit_of_work import UnitOfWork
from app.services.auth_service import AuthService
from app.services.excel_service import ExcelReportService
from app.services.permissions import modules_for_role
from app.services.report_service import InvoicePdfService

from .ui_inventory_list import Ui_InventoryWindow
from .ui_invoice_entry import Ui_InvoiceWindow
from .ui_login import Ui_LoginDialog
from .ui_main_menu import Ui_MainWindow
from .ui_purchase_orders import Ui_PurchaseWindow
from .ui_reports_menu import Ui_ReportsWindow


class InventoryWindow(QtWidgets.QMainWindow, Ui_InventoryWindow):
    def __init__(self, uow: UnitOfWork):
        super().__init__()
        self.setupUi(self)
        self.uow = uow
        self.model = QtGui.QStandardItemModel(self)
        self.inventoryTable.setModel(self.model)
        self.addButton.clicked.connect(self.create_item)
        self.editButton.clicked.connect(self.rename_item)
        self.deleteButton.clicked.connect(self.delete_item)
        self.refresh()

    def refresh(self) -> None:
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["SKU", "Name", "Quantity", "Unit Price"])
        for item in self.uow.stock_items.list():
            unit_price = float(item.unit_price or 0)
            row = [
                QtGui.QStandardItem(item.sku),
                QtGui.QStandardItem(item.name),
                QtGui.QStandardItem(str(item.quantity)),
                QtGui.QStandardItem(f"{unit_price:.2f}"),
            ]
            self.model.appendRow(row)

    def _selected_item(self):
        index = self.inventoryTable.currentIndex()
        if not index.isValid():
            return None
        sku = self.model.item(index.row(), 0).text()
        for item in self.uow.stock_items.list():
            if item.sku == sku:
                return item
        return None

    def create_item(self) -> None:
        sku, ok = QtWidgets.QInputDialog.getText(self, "SKU", "Enter SKU")
        if not ok or not sku:
            return
        name, ok = QtWidgets.QInputDialog.getText(self, "Name", "Enter name")
        if not ok or not name:
            return
        warehouse = self.uow.warehouses.session.query(self.uow.warehouses.model).first()
        if not warehouse:
            warehouse = self.uow.warehouses.model(name="Default Warehouse")
            self.uow.warehouses.add(warehouse)
            self.uow.session.flush()
        item = self.uow.stock_items.model(
            sku=sku,
            name=name,
            quantity=0,
            unit_price=0,
            warehouse_id=warehouse.id,
        )
        self.uow.stock_items.add(item)
        self.uow.session.commit()
        self.refresh()

    def rename_item(self) -> None:
        item = self._selected_item()
        if not item:
            return
        new_name, ok = QtWidgets.QInputDialog.getText(self, "Rename", "New name", text=item.name)
        if not ok or not new_name:
            return
        self.uow.stock_items.update(item, name=new_name)
        self.uow.session.commit()
        self.refresh()

    def delete_item(self) -> None:
        item = self._selected_item()
        if not item:
            return
        self.uow.stock_items.delete(item)
        self.uow.session.commit()
        self.refresh()


class PurchaseWindow(QtWidgets.QMainWindow, Ui_PurchaseWindow):
    def __init__(self, uow: UnitOfWork):
        super().__init__()
        self.setupUi(self)
        self.uow = uow
        self.model = QtGui.QStandardItemModel(self)
        self.ordersTable.setModel(self.model)
        self.newOrderButton.clicked.connect(self.create_order)
        self.receiveButton.clicked.connect(self.mark_received)
        self.cancelButton.clicked.connect(self.cancel_order)
        self.refresh()

    def refresh(self) -> None:
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["ID", "Supplier", "Status"])
        for order in self.uow.purchase_orders.list():
            supplier = order.supplier.name if order.supplier else "Unknown"
            row = [
                QtGui.QStandardItem(str(order.id)),
                QtGui.QStandardItem(supplier),
                QtGui.QStandardItem(order.status),
            ]
            self.model.appendRow(row)

    def _selected_order(self):
        index = self.ordersTable.currentIndex()
        if not index.isValid():
            return None
        order_id = int(self.model.item(index.row(), 0).text())
        return self.uow.purchase_orders.get(order_id)

    def create_order(self) -> None:
        supplier_name, ok = QtWidgets.QInputDialog.getText(self, "Supplier", "Enter supplier name")
        if not ok or not supplier_name:
            return
        supplier = self.uow.suppliers.session.query(self.uow.suppliers.model).filter_by(name=supplier_name).one_or_none()
        if not supplier:
            supplier = self.uow.suppliers.model(name=supplier_name)
            self.uow.suppliers.add(supplier)
            self.uow.session.flush()
        order = self.uow.purchase_orders.model(supplier_id=supplier.id, status="draft")
        self.uow.purchase_orders.add(order)
        self.uow.session.commit()
        self.refresh()

    def mark_received(self) -> None:
        order = self._selected_order()
        if not order:
            return
        self.uow.purchase_orders.update(order, status="received")
        self.uow.session.commit()
        self.refresh()

    def cancel_order(self) -> None:
        order = self._selected_order()
        if not order:
            return
        self.uow.purchase_orders.update(order, status="cancelled")
        self.uow.session.commit()
        self.refresh()


class InvoiceWindow(QtWidgets.QMainWindow, Ui_InvoiceWindow):
    def __init__(self, uow: UnitOfWork, pdf_service: InvoicePdfService):
        super().__init__()
        self.setupUi(self)
        self.uow = uow
        self.pdf_service = pdf_service
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Description", "Quantity", "Unit Price"])
        self.invoiceTable.setModel(self.model)
        self.addLineButton.clicked.connect(self.add_line)
        self.removeLineButton.clicked.connect(self.remove_line)
        self.saveInvoiceButton.clicked.connect(self.save_invoice)
        self.exportPdfButton.clicked.connect(self.export_pdf)
        self.load_customers()

    def load_customers(self) -> None:
        self.customerCombo.clear()
        for customer in self.uow.customers.list():
            self.customerCombo.addItem(customer.name, customer.id)

    def add_line(self) -> None:
        desc, ok = QtWidgets.QInputDialog.getText(self, "Description", "Line description")
        if not ok or not desc:
            return
        qty, ok = QtWidgets.QInputDialog.getInt(self, "Quantity", "Quantity", 1, 1)
        if not ok:
            return
        price, ok = QtWidgets.QInputDialog.getDouble(self, "Unit price", "Unit price", 0, 0)
        if not ok:
            return
        row = [
            QtGui.QStandardItem(desc),
            QtGui.QStandardItem(str(qty)),
            QtGui.QStandardItem(f"{price:.2f}"),
        ]
        self.model.appendRow(row)

    def remove_line(self) -> None:
        index = self.invoiceTable.currentIndex()
        if index.isValid():
            self.model.removeRow(index.row())

    def save_invoice(self) -> None:
        customer_id = self.customerCombo.currentData()
        if customer_id is None:
            QtWidgets.QMessageBox.warning(self, "Invoice", "Select a customer")
            return
        invoice = self.uow.invoices.model(customer_id=customer_id, status="draft")
        self.uow.invoices.add(invoice)
        self.uow.session.flush()
        default_item = self.uow.stock_items.session.query(self.uow.stock_items.model).first()
        if not default_item:
            warehouse = self.uow.warehouses.session.query(self.uow.warehouses.model).first()
            if not warehouse:
                warehouse = self.uow.warehouses.model(name="Default Warehouse")
                self.uow.warehouses.add(warehouse)
                self.uow.session.flush()
            default_item = self.uow.stock_items.model(
                sku="AUTO",
                name="Auto Item",
                quantity=0,
                unit_price=0,
                warehouse_id=warehouse.id,
            )
            self.uow.stock_items.add(default_item)
            self.uow.session.flush()
        for row in range(self.model.rowCount()):
            description = self.model.item(row, 0).text()
            quantity = int(self.model.item(row, 1).text())
            unit_price = float(self.model.item(row, 2).text())
            line = self.uow.invoice_lines.model(
                invoice_id=invoice.id,
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                stock_item_id=default_item.id,
            )
            self.uow.invoice_lines.add(line)
        self.uow.session.commit()
        QtWidgets.QMessageBox.information(self, "Invoice", "Invoice saved")

    def export_pdf(self) -> None:
        customer_id = self.customerCombo.currentData()
        if customer_id is None:
            return
        invoice = self.uow.invoices.session.query(self.uow.invoices.model).filter_by(customer_id=customer_id).order_by(self.uow.invoices.model.id.desc()).first()
        if not invoice:
            QtWidgets.QMessageBox.warning(self, "Invoice", "No invoice to export")
            return
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", str(Path.cwd() / "invoice.pdf"), "PDF Files (*.pdf)")[0]
        if not path:
            return
        self.pdf_service.build(invoice, Path(path))
        QtWidgets.QMessageBox.information(self, "Invoice", "PDF exported")


class ReportsWindow(QtWidgets.QMainWindow, Ui_ReportsWindow):
    def __init__(self, uow: UnitOfWork, excel_service: ExcelReportService):
        super().__init__()
        self.setupUi(self)
        self.uow = uow
        self.excel_service = excel_service
        self.runReportButton.clicked.connect(self.run_report)
        self.exportExcelButton.clicked.connect(self.export_excel)
        self.refresh()

    def refresh(self) -> None:
        self.reportsList.clear()
        for report in self.uow.report_definitions.list():
            item = QtWidgets.QListWidgetItem(report.name)
            item.setData(QtCore.Qt.UserRole, report.id)
            self.reportsList.addItem(item)

    def _selected_report(self):
        item = self.reportsList.currentItem()
        if not item:
            return None
        report_id = item.data(QtCore.Qt.UserRole)
        return self.uow.report_definitions.get(report_id)

    def run_report(self) -> None:
        report = self._selected_report()
        if not report:
            return
        QtWidgets.QMessageBox.information(self, "Report", f"Would run SQL: {report.query}")

    def export_excel(self) -> None:
        report = self._selected_report()
        if not report:
            return
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save Excel", str(Path.cwd() / "report.xlsx"), "Excel Files (*.xlsx)"
                                                    )[0]
        if not path:
            return
        rows = [{"query": report.query, "name": report.name}]
        self.excel_service.export(rows, Path(path))
        QtWidgets.QMessageBox.information(self, "Report", "Excel exported")


class LoginDialog(QtWidgets.QDialog, Ui_LoginDialog):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.setupUi(self)
        self.auth_service = auth_service
        self.loginButton.clicked.connect(self.authenticate)
        self.accepted_user = None

    def authenticate(self) -> None:
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        user = self.auth_service.verify_credentials(username, password)
        if not user:
            self.errorLabel.setText("Invalid credentials")
            return
        self.accepted_user = user
        self.accept()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.inventory_window = None
        self.purchase_window = None
        self.invoice_window = None
        self.reports_window = None
        self.logoutButton.clicked.connect(self.close)

    def configure(self, session, allowed_modules: Iterable[str]) -> None:
        uow = UnitOfWork(session)
        self.inventory_window = InventoryWindow(uow)
        self.purchase_window = PurchaseWindow(uow)
        self.invoice_window = InvoiceWindow(uow, InvoicePdfService())
        self.reports_window = ReportsWindow(uow, ExcelReportService())

        self.inventoryButton.clicked.connect(self.inventory_window.show)
        self.purchasingButton.clicked.connect(self.purchase_window.show)
        self.invoicingButton.clicked.connect(self.invoice_window.show)
        self.reportsButton.clicked.connect(self.reports_window.show)

        self.inventoryButton.setEnabled("inventory" in allowed_modules)
        self.purchasingButton.setEnabled("purchasing" in allowed_modules)
        self.invoicingButton.setEnabled("invoicing" in allowed_modules)
        self.reportsButton.setEnabled("reports" in allowed_modules)


def launch_app() -> None:
    app = QtWidgets.QApplication([])
    session = SessionLocal()
    try:
        auth = AuthService(session)
        login = LoginDialog(auth)
        if login.exec() != QtWidgets.QDialog.Accepted:
            return
        modules = modules_for_role(login.accepted_user.role.name)
        main_window = MainWindow()
        main_window.configure(session, modules)
        main_window.show()
        app.exec()
    finally:
        session.close()
