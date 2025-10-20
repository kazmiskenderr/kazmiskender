"""Unit-of-work style repository facade for the application."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.inventory.models import InventoryTransaction, StockItem, Warehouse
from app.purchasing.models import PurchaseOrder, PurchaseOrderItem, Supplier
from app.invoicing.models import Customer, Invoice, InvoiceLine
from app.reports.models import ReportDefinition
from app.users.models import Role, User

from .base import Repository


class UnitOfWork:
    """Expose repositories grouped by business modules."""

    def __init__(self, session: Session):
        self.session = session
        # Inventory
        self.warehouses = Repository[Warehouse](session, Warehouse)
        self.stock_items = Repository[StockItem](session, StockItem)
        self.inventory_transactions = Repository[InventoryTransaction](session, InventoryTransaction)
        # Purchasing
        self.suppliers = Repository[Supplier](session, Supplier)
        self.purchase_orders = Repository[PurchaseOrder](session, PurchaseOrder)
        self.purchase_order_items = Repository[PurchaseOrderItem](session, PurchaseOrderItem)
        # Invoicing
        self.customers = Repository[Customer](session, Customer)
        self.invoices = Repository[Invoice](session, Invoice)
        self.invoice_lines = Repository[InvoiceLine](session, InvoiceLine)
        # Reports
        self.report_definitions = Repository[ReportDefinition](session, ReportDefinition)
        # Users
        self.roles = Repository[Role](session, Role)
        self.users = Repository[User](session, User)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
