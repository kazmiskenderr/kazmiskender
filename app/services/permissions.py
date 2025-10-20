"""Role-based permission helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(frozen=True)
class RolePermissions:
    role: str
    modules: Iterable[str]


DEFAULT_PERMISSIONS: Dict[str, RolePermissions] = {
    "admin": RolePermissions(role="admin", modules=("inventory", "purchasing", "invoicing", "reports", "users")),
    "manager": RolePermissions(role="manager", modules=("inventory", "purchasing", "invoicing", "reports")),
    "clerk": RolePermissions(role="clerk", modules=("inventory", "purchasing", "invoicing")),
    "viewer": RolePermissions(role="viewer", modules=("inventory", "reports")),
}


def modules_for_role(role_name: str) -> Iterable[str]:
    permissions = DEFAULT_PERMISSIONS.get(role_name.lower())
    if not permissions:
        return ()
    return permissions.modules
