import logging
from json import dumps
from typing import List

import json_fix

from dotty.profile_storage import ProfileStorage
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


class UserRegistry:
    def __init__(self, profile_storage: ProfileStorage):
        self._storage_name = "user_register.json"
        self._profile_storage = profile_storage
        self._all_users: List[User] = []
        profiles = self._profile_storage.retrieve_profiles()
        if profiles:
            for profile in profiles:
                security_level_value = int(profile["security_level"])
                self._all_users.append(
                    User(identifier=profile["identifier"], security_level=SecurityLevel(security_level_value))
                )

    def register_user(self, identifier: str, role: SecurityLevel) -> None:
        logging.debug(f"Register user: {identifier}, {role}")
        if self.is_registered_user(identifier=identifier):
            user = self.get_user(identifier=identifier)
            user.set_security_level(security_level=role)
        else:
            self._all_users.append(User(identifier=identifier, security_level=role))
        self._profile_storage.store_profiles(users=self._all_users)

    def is_registered_user(self, identifier: str) -> bool:
        return identifier in [user.get_user_identifier() for user in self._all_users]

    def get_user(self, identifier: str) -> User:
        return [user for user in self._all_users if user.get_user_identifier() == identifier].pop()
