from typing import List, Optional

from dotty.command_identifier import CommandIdentifier
from dotty.command_type import CommandType
from dotty.security_level import SecurityLevel


class Command:
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        self._trigger: str = trigger
        self._description: str = description
        self.identifier: CommandIdentifier = identifier
        self._type: CommandType = CommandType.UNSET
        self._security_level: SecurityLevel = security_level

    def __repr__(self):
        return f'"{self._trigger}" - {self._description}'

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        pass

    def get_trigger(self) -> str:
        return self._trigger

    def get_trigger_lower_case(self) -> str:
        return self._trigger.casefold()

    def is_substitution(self):
        return self._type == CommandType.SUBSTITUTION

    def has_clearance(self, requested_by: SecurityLevel):
        return requested_by >= self._security_level

    def get_security_level(self):
        return self._security_level


class StartsWithCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, description, security_level)
        self._type: CommandType = CommandType.STARTS_WITH

    def has_match(self, message: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        return message.casefold().startswith(self.get_trigger_lower_case())


class ContainsCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, description, security_level)
        self._type: CommandType = CommandType.CONTAINS

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        return self.get_trigger_lower_case() in message_body.casefold()


class ExactCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, description, security_level)
        self._type: CommandType = CommandType.EXACT

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        return self.get_trigger_lower_case() == message_body.casefold()


class SubstitutionCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, substitution: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, "substitution", security_level)
        self._type: CommandType = CommandType.SUBSTITUTION
        self._substitution = substitution

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        return self.get_trigger_lower_case() == message_body.casefold()

    def __repr__(self):
        return self._substitution
