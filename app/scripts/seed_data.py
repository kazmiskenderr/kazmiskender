"""Seed the database with default users, roles, and report definitions."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.inventory.models import Warehouse
from app.reports.models import ReportDefinition
from app.services.auth_service import AuthService
from app.users.models import Role, User


def ensure_roles(session: Session) -> None:
    for role_name in ("admin", "manager", "clerk", "viewer"):
        if not session.query(Role).filter_by(name=role_name).first():
            session.add(Role(name=role_name))
    session.commit()


def ensure_admin(session: Session) -> None:
    auth = AuthService(session)
    role = session.query(Role).filter_by(name="admin").first()
    if not role:
        role = Role(name="admin")
        session.add(role)
        session.flush()
    if not session.query(User).filter_by(username="admin").first():
        auth.create_user("admin", "admin", role.id)


def ensure_reports(session: Session) -> None:
    if not session.query(ReportDefinition).first():
        session.add(
            ReportDefinition(
                name="Inventory Summary",
                description="Shows total stock per SKU",
                query="SELECT sku, SUM(quantity) AS total_quantity FROM stock_items GROUP BY sku",
            )
        )
        session.commit()


def ensure_warehouse(session: Session) -> None:
    if not session.query(Warehouse).first():
        session.add(Warehouse(name="Default Warehouse"))
        session.commit()


def main() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        ensure_roles(session)
        ensure_admin(session)
        ensure_reports(session)
        ensure_warehouse(session)


if __name__ == "__main__":
    main()
