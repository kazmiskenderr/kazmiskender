from __future__ import annotations

import pytest

sqlalchemy = pytest.importorskip("sqlalchemy")

create_engine = sqlalchemy.create_engine
sessionmaker = sqlalchemy.orm.sessionmaker

from app.database import Base
from app.services.auth_service import AuthService
from app.users.models import Role


def create_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)()


def test_authenticate_user():
    session = create_session()
    role = Role(name="admin")
    session.add(role)
    session.commit()
    auth = AuthService(session)
    user = auth.create_user("alice", "password", role.id)
    assert auth.verify_credentials("alice", "password") == user
    assert auth.verify_credentials("alice", "wrong") is None
