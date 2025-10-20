"""Services for generating PDF invoices using ReportLab."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.invoicing.models import Invoice, InvoiceLine


@dataclass
class InvoiceLineData:
    description: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class InvoiceDocument:
    invoice_number: str
    customer_name: str
    customer_address: str | None
    lines: Iterable[InvoiceLineData]

    @property
    def total(self) -> float:
        return sum(line.total for line in self.lines)


class InvoicePdfService:
    """Generate PDF documents for invoices using ReportLab."""

    def build(self, invoice: Invoice, output_path: Path) -> Path:
        document = InvoiceDocument(
            invoice_number=str(invoice.id),
            customer_name=invoice.customer.name,
            customer_address=invoice.customer.address,
            lines=[
                InvoiceLineData(
                    description=line.description,
                    quantity=line.quantity,
                    unit_price=float(line.unit_price),
                )
                for line in invoice.lines
            ],
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(output_path), pagesize=A4)
        width, height = A4
        y = height - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, f"Invoice #{document.invoice_number}")
        y -= 30
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Customer: {document.customer_name}")
        y -= 20
        if document.customer_address:
            c.drawString(50, y, f"Address: {document.customer_address}")
            y -= 20

        c.drawString(50, y, "Description")
        c.drawString(300, y, "Qty")
        c.drawString(350, y, "Unit Price")
        c.drawString(450, y, "Total")
        y -= 20

        for line in document.lines:
            c.drawString(50, y, line.description)
            c.drawRightString(320, y, str(line.quantity))
            c.drawRightString(420, y, f"{line.unit_price:.2f}")
            c.drawRightString(520, y, f"{line.total:.2f}")
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(520, y - 10, f"Grand Total: {document.total:.2f}")
        c.showPage()
        c.save()
        return output_path
