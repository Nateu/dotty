from typing import Optional

from src.dotty.command import Command
from src.dotty.command_identifier import CommandIdentifier
from src.dotty.command_registry import CommandRegistry
from src.dotty.message import Message
from src.dotty.security_level import SecurityLevel
from src.dotty.user_registry import UserRegistry


class ChatBot:
    def __init__(self, name: str, owner_identifier: str, users_registry: UserRegistry, command_registry: CommandRegistry):
        self._name: str = name
        self._theme: str = "No theme set"
        self._users_registry = users_registry
        self._users_registry.register_user(owner_identifier, SecurityLevel.OWNER)
        self._command_registry = command_registry

    def update_user(self, user_jid, role: SecurityLevel = SecurityLevel.UNKNOWN):
        if not self._users_registry.is_registered_user(identifier=user_jid):
            self._users_registry.register_user(identifier=user_jid, role=role)

    def process_message(self, message: Message) -> str:
        user_security_level = self._get_user_security_level(message.sent_by)
        command = self._command_registry.get_matching_command(message.body, user_security_level)
        if command:
            return self._process_command(command, message, user_security_level)

    def _get_user_security_level(self, user_identifier) -> SecurityLevel:
        if self._users_registry.is_registered_user(user_identifier):
            return self._users_registry.get_user(user_identifier).get_user_clearance_level()
        return SecurityLevel.GUEST

    def _process_command(self, command: Command, message: Message, user_security_level: SecurityLevel) -> Optional[str]:
        if command.identifier == CommandIdentifier.LIST_COMMANDS:
            return self._list_commands(user_security_level=user_security_level)
        if command.identifier == CommandIdentifier.SET_USER_SUBSTITUTION:
            return self._set_substitution(command=command, message_body=message.body, security_level=SecurityLevel.USER)
        if command.identifier == CommandIdentifier.SET_ADMIN_SUBSTITUTION:
            return self._set_substitution(command=command, message_body=message.body, security_level=SecurityLevel.ADMIN)
        if command.identifier == CommandIdentifier.LIST_SUBSTITUTIONS:
            return self._list_substitutions(user_security_level=user_security_level)
        if command.identifier == CommandIdentifier.GET_SUBSTITUTION:
            return str(command)
        if command.identifier == CommandIdentifier.LIST_USERS:
            return self._list_users()
        if command.identifier == CommandIdentifier.SET_THEME:
            return self._set_theme(command=command, message_body=message.body)
        if command.identifier == CommandIdentifier.GET_THEME:
            return self._get_theme()
        if command.identifier == CommandIdentifier.SET_ROLE_OWNER:
            return self._set_role(command=command, message_body=message.body, destination_role=SecurityLevel.OWNER)
        if command.identifier == CommandIdentifier.REMOVE_ROLE_OWNER:
            return self._set_role(command=command, message_body=message.body, destination_role=SecurityLevel.ADMIN, revoke=True)
        if command.identifier == CommandIdentifier.SET_ROLE_ADMIN:
            return self._set_role(command=command, message_body=message.body, destination_role=SecurityLevel.ADMIN)
        if command.identifier == CommandIdentifier.REMOVE_ROLE_ADMIN:
            return self._set_role(command=command, message_body=message.body, destination_role=SecurityLevel.USER, revoke=True)
        if command.identifier == CommandIdentifier.SET_ROLE_USER:
            return self._set_role(command=command, message_body=message.body, destination_role=SecurityLevel.USER)
        if command.identifier == CommandIdentifier.REMOVE_ROLE_USER:
            return self._set_role(command=command, message_body=message.body, destination_role=SecurityLevel.GUEST, revoke=True)

    def _list_users(self) -> str:
        return f"The current users\n{self._users_registry.get_user_listing()}"

    def _set_substitution(self, command: Command, message_body: str, security_level: SecurityLevel) -> Optional[str]:
        trigger, substitution = message_body.split(command.get_trigger())
        new_command = self._command_registry.register_substitution(
            trigger=trigger, substitution=substitution, security_level=security_level
        )
        if not new_command:
            return
        return f'When you say: "{new_command.get_trigger()}", I say: {new_command}'

    def _get_theme(self) -> str:
        return self._theme

    def _set_theme(self, command: Command, message_body: str) -> str:
        self._theme = message_body[len(command.get_trigger()) :]
        return f"Theme set to: {self._theme}"

    def _list_substitutions(self, user_security_level: SecurityLevel) -> str:
        substitutions_string = self._command_registry.get_substitution_listing(user_security_level)
        return f"These substitutions are set: {substitutions_string}"

    def _list_commands(self, user_security_level: SecurityLevel) -> str:
        commands_string = self._command_registry.get_commands_string(user_security_level=user_security_level)
        return f"These commands are available:\n{commands_string}"

    def _set_role(self, command: Command, message_body: str, destination_role: SecurityLevel, revoke: bool = False) -> str:
        user_identifier = message_body[len(command.get_trigger()) :]
        user_role = self._get_user_security_level(user_identifier)
        if revoke:
            if user_role < destination_role:
                return "Rights already revoked"
            self._users_registry.register_user(user_identifier, destination_role)
            return "Rights revoked"
        else:
            if user_role >= destination_role:
                return "User already registered"
            self._users_registry.register_user(user_identifier, destination_role)
            return "User registered"
