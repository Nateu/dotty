from typing import List

from dotty.command import Command, CommandRegistry
from dotty.profile_storage import ProfileStorage
from dotty.user import User
from dotty.user_registry import UserRegistry


class FakeUser(User):
    def __init__(self):
        self.get_user_identifier_response = ""
        self.get_user_clearance_level_response = ""

    def get_user_identifier(self):
        return self.get_user_identifier_response

    def get_user_clearance_level(self):
        return self.get_user_clearance_level_response

    def set_security_level(self, security_level):
        pass


class FakeUserRegistry(UserRegistry):
    def __init__(self):
        self.is_registered_user_outcome = True
        self.get_user_response = ""

    def register_user(self, identifier, role):
        pass

    def is_registered_user(self, identifier):
        return self.is_registered_user_outcome

    def get_user(self, identifier):
        return self.get_user_response


class FakeCommand(Command):
    def __init__(self):
        self.repr_response = ""
        self.has_match_response = True
        self.get_trigger_response = ""
        self.is_substitution_response = True
        self.has_clearance_response = True
        self.get_security_level_response = ""
        self.identifier = ""

    def __repr__(self):
        return self.repr_response

    def has_match(self, message_body, user_security_level):
        return self.has_match_response

    def get_trigger(self):
        return self.get_trigger_response

    def get_trigger_lower_case(self):
        return self.get_trigger_response.casefold()

    def is_substitution(self):
        return self.is_substitution_response

    def has_clearance(self, requested_by):
        return self.has_clearance_response

    def get_security_level(self):
        return self.get_security_level_response


class FakeCommandRegistry(CommandRegistry):
    def __init__(self):
        self.all_commands_response = ""
        self.get_matching_command_response = None
        self.get_commands_string_response = ""
        self.get_substitution_listing_response = ""
        self.register_substitution_response = None

    def get_all_commands(self):
        return self.all_commands_response

    def set_bot_name(self, bot_name):
        pass

    def get_matching_command(self, message, user_security_level):
        return self.get_matching_command_response

    def get_commands_string(self, user_security_level):
        return self.get_commands_string_response

    def get_substitution_listing(self, user_security_level):
        return self.get_substitution_listing_response

    def register_substitution(self, trigger, substitution, security_level):
        return self.register_substitution_response


class FakeProfileStorage(ProfileStorage):
    def __init__(self):
        self.retrieve_profiles_response = ""

    def create_owner(self, identifier: str) -> None:
        pass

    def store_profiles(self, users: List[User]) -> None:
        pass

    def retrieve_profiles(self) -> List[User]:
        return self.retrieve_profiles_response
