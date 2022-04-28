import json_fix

from dotty.security_level import SecurityLevel


class User:
    def __init__(self, identifier: str, security_level: SecurityLevel):
        self._identifier: str = identifier
        self._security_level: SecurityLevel = security_level

    def __json__(self):
        return {"identifier": self._identifier, "security level": self._security_level}

    def get_user_identifier(self) -> str:
        return self._identifier

    def get_user_clearance_level(self) -> SecurityLevel:
        return self._security_level

    def set_security_level(self, security_level: SecurityLevel) -> None:
        self._security_level = security_level
