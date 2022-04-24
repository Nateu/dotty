import logging
from enum import Enum, auto
from typing import List

from dotty.security_level import SecurityLevel
from dotty.user import UserRegistry


class CommandType(Enum):
    CONTAINS = auto()
    EXACT = auto()
    SUBSTITUTION = auto()
    STARTS_WITH = auto()
    UNSET = auto()


class CommandIdentifier(Enum):
    GET_SUBSTITUTION = auto()
    GET_THEME = auto()
    LIST_COMMANDS = auto()
    LIST_SUBSTITUTIONS = auto()
    SET_ROLE_ADMIN = auto()
    SET_ROLE_OWNER = auto()
    SET_ROLE_USER = auto()
    SET_ADMIN_SUBSTITUTION = auto()
    SET_USER_SUBSTITUTION = auto()
    SET_THEME = auto()
    REMOVE_ROLE_ADMIN = auto()
    REMOVE_ROLE_OWNER = auto()
    REMOVE_ROLE_USER = auto()


class Message:
    def __init__(self, body: str, sent_by: str, sent_in: str):
        self.sent_by: str = sent_by
        self.sent_in: str = sent_in
        self.body: str = body

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.body == other.body and self.sent_by == other.sent_by and self.sent_in == other.sent_in
        return False


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


class StartsWithCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, description, security_level)
        self._type: CommandType = CommandType.STARTS_WITH

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        logging.debug(f"Starts with: [{self.get_trigger_lower_case()}] > [{message_body.casefold()}]")
        return message_body.casefold().startswith(self.get_trigger_lower_case())


class ContainsCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, description, security_level)
        self._type: CommandType = CommandType.CONTAINS

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        logging.debug(f"Checking: [{self.get_trigger_lower_case()}] in [{message_body.casefold()}]")
        return self.get_trigger_lower_case() in message_body.casefold()


class ExactCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, description, security_level)
        self._type: CommandType = CommandType.EXACT

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        logging.debug(
            f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] {self.get_trigger_lower_case() == message_body.casefold()}"
        )
        return self.get_trigger_lower_case() == message_body.casefold()


class SubstitutionCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, substitution: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, "substitution", security_level)
        self._type: CommandType = CommandType.SUBSTITUTION
        self._substitution = substitution

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        logging.debug(
            f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] {self.get_trigger_lower_case() == message_body.casefold()}"
        )
        return self.get_trigger_lower_case() == message_body.casefold()

    def __repr__(self):
        return self._substitution


class ChatBot:
    def __init__(self, name: str, owner_identifier: str, users_registry: UserRegistry):
        self._name: str = name
        self._theme: str = "No theme set"
        self._users_registry = users_registry
        self._users_registry.register_user(owner_identifier, SecurityLevel.OWNER)
        self._all_commands: List[Command] = []
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.LIST_COMMANDS, "Usage", "List all commands and their usage", SecurityLevel.USER
            )
        )
        self._all_commands.append(
            ExactCommand(CommandIdentifier.LIST_SUBSTITUTIONS, "List", "List all substitutions", SecurityLevel.USER)
        )
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_USER_SUBSTITUTION,
                " -> ",
                f"On the trigger (before) -> {self._name} will respond with message (after) [USERS]",
                SecurityLevel.ADMIN,
            )
        )
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_ADMIN_SUBSTITUTION,
                " => ",
                f"On the trigger (before) => {self._name} will respond with message (after) [ADMINS]",
                SecurityLevel.ADMIN,
            )
        )
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.GET_THEME, "Theme", "This will give back the current theme", SecurityLevel.USER
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_THEME,
                "Set Theme ",
                'This will set a theme, anything after "set theme " will be the theme',
                SecurityLevel.ADMIN,
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_ROLE_USER,
                "Grant User ",
                "Command to grant a member user status",
                SecurityLevel.ADMIN,
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_ROLE_ADMIN,
                "Grant Admin ",
                "Command to grant a member admin status",
                SecurityLevel.OWNER,
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_ROLE_OWNER,
                "Grant Owner ",
                "Command to grant a member owner status",
                SecurityLevel.OWNER,
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.REMOVE_ROLE_OWNER,
                "Revoke Owner ",
                "Command to revoke a member owner status",
                SecurityLevel.OWNER,
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.REMOVE_ROLE_ADMIN,
                "Revoke Admin ",
                "Command to revoke a member admin status",
                SecurityLevel.OWNER,
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.REMOVE_ROLE_USER,
                "Revoke User ",
                "Command to revoke a member user status",
                SecurityLevel.ADMIN,
            )
        )

    def process_message(self, message: Message) -> str:
        user_security_level = self._get_user_security_level(message.sent_by)
        logging.debug(f"User: {message.sent_by}, {user_security_level}")
        for command in self._all_commands:
            logging.debug(f"Checking Command: {command.get_trigger()}")
            if command.has_match(message.body, user_security_level):
                logging.debug(f"Found a match: {command.get_trigger_lower_case()}")
                return self._process_command(command, message)

    def _get_user_security_level(self, user_identifier):
        if self._users_registry.is_registered_user(user_identifier):
            return self._users_registry.get_user(user_identifier).get_user_clearance_level()
        return SecurityLevel.GUEST

    def _process_command(self, command: Command, message: Message) -> str:
        match command.identifier:
            case CommandIdentifier.LIST_COMMANDS:
                return self._list_commands(message.sent_by)
            case CommandIdentifier.LIST_SUBSTITUTIONS:
                return self._list_substitutions(message.sent_by)
            case CommandIdentifier.GET_SUBSTITUTION:
                return self._get_substitution(command)
            case CommandIdentifier.SET_THEME:
                return self._set_theme(command, message.body)
            case CommandIdentifier.GET_THEME:
                return self._get_theme()
            case CommandIdentifier.SET_USER_SUBSTITUTION:
                return self._set_substitution(command, message.body, SecurityLevel.USER)
            case CommandIdentifier.SET_ADMIN_SUBSTITUTION:
                return self._set_substitution(command, message.body, SecurityLevel.ADMIN)
            case CommandIdentifier.SET_ROLE_USER:
                return self._set_role(command, message.body, SecurityLevel.USER)
            case CommandIdentifier.SET_ROLE_ADMIN:
                return self._set_role(command, message.body, SecurityLevel.ADMIN)
            case CommandIdentifier.SET_ROLE_OWNER:
                return self._set_role(command, message.body, SecurityLevel.OWNER)
            case CommandIdentifier.REMOVE_ROLE_OWNER:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.ADMIN, revoke=True)
            case CommandIdentifier.REMOVE_ROLE_ADMIN:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.USER, revoke=True)
            case CommandIdentifier.REMOVE_ROLE_USER:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.GUEST, revoke=True)

    def _set_substitution(self, command: Command, message_body: str, security_level: SecurityLevel) -> str:
        trigger, substitution = message_body.split(command.get_trigger())
        logging.debug(f"Set substitution {trigger}")
        self._all_commands.append(
            SubstitutionCommand(CommandIdentifier.GET_SUBSTITUTION, trigger, substitution, security_level)
        )
        return f'When you say: "{trigger}", I say: {substitution}'

    def _get_substitution(self, command: Command) -> str:
        logging.debug(f"Get substitution: {command}")
        return str(command)

    def _get_theme(self) -> str:
        logging.debug(f"Get theme {self._theme}")
        return self._theme

    def _set_theme(self, command: Command, message_body: str) -> str:
        self._theme = message_body[len(command.get_trigger()) :]
        logging.debug(f"Set theme: {self._theme}")
        return f"Theme set to: {self._theme}"

    def _list_substitutions(self, user_identifier: str) -> str:
        logging.debug("List all substitutions")
        substitutions_string = ", ".join(
            [
                command.get_trigger()
                for command in self._all_commands
                if command.has_clearance(self._get_user_security_level(user_identifier)) and command.is_substitution()
            ]
        )
        return f"These substitutions are set: {substitutions_string}"

    def _list_commands(self, user_identifier: str) -> str:
        logging.debug("List commands")
        commands_string = "".join(
            [
                f"{command}\n"
                for command in self._all_commands
                if command.has_clearance(self._get_user_security_level(user_identifier))
                and not command.is_substitution()
            ]
        )
        return f"These commands are available:\n{commands_string}"

    def _set_role(self, command: Command, message_body: str, role: SecurityLevel, revoke: bool = False) -> str:
        user_identifier = message_body[len(command.get_trigger()) :]
        if revoke:
            if self._get_user_security_level(user_identifier) < role:
                return "Rights already revoked"
            self._users_registry.register_user(user_identifier, role)
            return "Rights revoked"
        else:
            if self._get_user_security_level(user_identifier) >= role:
                return "User already registered"
            self._users_registry.register_user(user_identifier, role)
            return "User registered"
