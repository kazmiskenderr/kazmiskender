"""Generic repository implementation for CRUD operations."""
from __future__ import annotations

from typing import Generic, Iterable, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class Repository(Generic[T]):
    """Generic CRUD helper bound to a SQLAlchemy session."""

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def add(self, instance: T) -> T:
        self.session.add(instance)
        return instance

    def get(self, ident: int) -> Optional[T]:
        return self.session.get(self.model, ident)

    def list(self) -> List[T]:
        return list(self.session.scalars(select(self.model)))

    def delete(self, instance: T) -> None:
        self.session.delete(instance)

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.session.add(instance)
        return instance

    def add_all(self, instances: Iterable[T]) -> None:
        self.session.add_all(list(instances))
