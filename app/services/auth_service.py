"""Authentication helpers for the login UI."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from app.users.models import User


class AuthService:
    """Authenticate users against the database."""

    def __init__(self, session: Session):
        self.session = session

    def verify_credentials(self, username: str, password: str) -> Optional[User]:
        user = self.session.query(User).filter(User.username == username, User.is_active.is_(True)).one_or_none()
        if user and check_password_hash(user.password_hash, password):
            user.last_login_at = datetime.utcnow()
            self.session.add(user)
            self.session.commit()
            return user
        return None

    def create_user(self, username: str, password: str, role_id: int) -> User:
        user = User(username=username, password_hash=generate_password_hash(password), role_id=role_id)
        self.session.add(user)
        self.session.commit()
        return user
