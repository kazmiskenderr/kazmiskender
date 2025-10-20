from __future__ import annotations

import pytest

sqlalchemy = pytest.importorskip("sqlalchemy")

create_engine = sqlalchemy.create_engine
sessionmaker = sqlalchemy.orm.sessionmaker

from app.database import Base
from app.inventory.models import StockItem, Warehouse
from app.repository.unit_of_work import UnitOfWork


def in_memory_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)()


def test_inventory_crud():
    session = in_memory_session()
    uow = UnitOfWork(session)
    warehouse = Warehouse(name="Main")
    uow.warehouses.add(warehouse)
    session.flush()

    item = StockItem(sku="SKU1", name="Item", quantity=5, unit_price=10, warehouse_id=warehouse.id)
    uow.stock_items.add(item)
    session.commit()

    saved = uow.stock_items.get(item.id)
    assert saved is not None
    assert saved.name == "Item"

    uow.stock_items.update(saved, name="Updated")
    session.commit()
    updated = uow.stock_items.get(item.id)
    assert updated.name == "Updated"

    uow.stock_items.delete(updated)
    session.commit()
    assert uow.stock_items.get(item.id) is None
