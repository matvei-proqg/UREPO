from enum import Enum
from typing import List

class Role(Enum):
    GUEST = "guest"
    DEVELOPER = "developer"
    MAINTAINER = "maintainer"
    ADMIN = "admin"

class RBAC:
    def __init__(self):
        self.permissions = {
            Role.GUEST: ["read:packages"],
            Role.DEVELOPER: ["read:packages", "create:packages", "update:own_packages"],
            Role.MAINTAINER: ["read:packages", "create:packages", "update:packages", "delete:packages"],
            Role.ADMIN: ["*"]
        }

    def has_permission(self, role: Role, permission: str) -> bool:
        if role not in self.permissions:
            return False
        return permission in self.permissions[role] or "*" in self.permissions[role]
