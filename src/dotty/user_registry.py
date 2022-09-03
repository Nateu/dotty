from typing import List

from dotty.profile_storage import ProfileStorage
from dotty.security_level import SecurityLevel
from dotty.statics import jid_to_username
from dotty.user import User


class UserRegistry:
    def __init__(self, profile_storage: ProfileStorage):
        self._profile_storage = profile_storage
        self._all_users: List[User] = self._profile_storage.retrieve_profiles()

    def register_user(self, identifier: str, role: SecurityLevel) -> None:
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

    def get_user_listing(self):
        return "\n".join(
            [f"{jid_to_username(user.get_user_identifier())}: {user.get_user_clearance_level().name}" for user in self._all_users]
        )
