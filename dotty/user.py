import json
import logging
from json import dumps
from typing import List

import json_fix

from dotty.security_level import SecurityLevel
from dotty.storage import Storage


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
    def __init__(self, storage: Storage):
        self._storage_name = "user_register.json"
        self._storage = storage
        self._all_users: List[User] = []
        data = self._storage.retrieve_data(self._storage_name)
        if data:
            json_data = json.loads(data)
            for user in json_data:
                self._all_users.append(
                    User(identifier=user["identifier"], security_level=SecurityLevel(user["security level"]))
                )

    def register_user(self, identifier: str, role: SecurityLevel) -> None:
        logging.debug(f"Register user: {identifier}, {role}")
        if self.is_registered_user(identifier=identifier):
            user = self.get_user(identifier=identifier)
            user.set_security_level(security_level=role)
        else:
            self._all_users.append(User(identifier=identifier, security_level=role))
        json_data = dumps([user for user in self._all_users])
        self._storage.store_in(data=json_data, storage_name=self._storage_name)

    def is_registered_user(self, identifier: str) -> bool:
        return identifier in [user.get_user_identifier() for user in self._all_users]

    def get_user(self, identifier: str) -> User:
        return [user for user in self._all_users if user.get_user_identifier() == identifier].pop()
