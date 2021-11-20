import logging
from enum import Enum, auto
from functools import total_ordering
from typing import List


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


@total_ordering
class SecurityLevel(Enum):
    OWNER = 9
    ADMIN = 7
    USER = 5
    GUEST = 3
    UNKNOWN = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


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
        logging.debug(f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] {self.get_trigger_lower_case() == message_body.casefold()}")
        return self.get_trigger_lower_case() == message_body.casefold()


class SubstitutionCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, substitution: str, security_level: SecurityLevel):
        super().__init__(identifier, trigger, "substitution", security_level)
        self._type: CommandType = CommandType.SUBSTITUTION
        self._substitution = substitution

    def has_match(self, message_body: str, user_security_level: SecurityLevel) -> bool:
        if not self.has_clearance(user_security_level):
            return False
        logging.debug(f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] {self.get_trigger_lower_case() == message_body.casefold()}")
        return self.get_trigger_lower_case() == message_body.casefold()

    def __repr__(self):
        return self._substitution


class User:
    def __init__(self, identifier: str, security_level: SecurityLevel):
        self._identifier: str = identifier
        self._security_level: SecurityLevel = security_level

    def get_user_identifier(self) -> str:
        return self._identifier

    def get_user_clearance_level(self) -> SecurityLevel:
        return self._security_level


class UserRegistry:
    def __init__(self):
        self._all_users: List[User] = []

    def register_user(self, identifier: str, role: SecurityLevel) -> None:
        logging.debug(f"Register user: {identifier}, {role}")
        self._all_users.append(User(identifier, role))

    def is_registered_user(self, identifier: str) -> bool:
        return identifier in [user.get_user_identifier() for user in self._all_users]

    def get_user(self, identifier: str) -> User:
        return [user for user in self._all_users if user.get_user_identifier() == identifier].pop()


class ChatBot:
    def __init__(self, name: str, owner_identifier: str):
        self._name: str = name
        self._theme: str = 'No theme set'
        self._users_registry = UserRegistry()
        self._users_registry.register_user(owner_identifier, SecurityLevel.OWNER)
        self._all_commands: List[Command] = []
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.LIST_COMMANDS,
                "Usage",
                "List all commands and their usage",
                SecurityLevel.USER
            )
        )
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.LIST_SUBSTITUTIONS,
                "List",
                "List all substitutions",
                SecurityLevel.USER
            )
        )
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_USER_SUBSTITUTION,
                " -> ",
                f"On the trigger (before) -> {self._name} will respond with message (after) [USERS]",
                SecurityLevel.ADMIN
            )
        )
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_ADMIN_SUBSTITUTION,
                " => ",
                f"On the trigger (before) => {self._name} will respond with message (after) [ADMINS]",
                SecurityLevel.ADMIN
            )
        )
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.GET_THEME,
                "Theme",
                "This will give back the current theme",
                SecurityLevel.USER
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_THEME,
                "Set Theme ",
                'This will set a theme, anything after "set theme " will be the theme',
                SecurityLevel.ADMIN
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_ROLE_USER,
                "Grant User ",
                'Command to grant a member user status',
                SecurityLevel.ADMIN
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_ROLE_ADMIN,
                "Grant Admin ",
                'Command to grant a member admin status',
                SecurityLevel.OWNER
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_ROLE_OWNER,
                "Grant Owner ",
                'Command to grant a member owner status',
                SecurityLevel.OWNER
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

    def _set_substitution(self, command: Command, message_body: str, security_level: SecurityLevel) -> str:
        trigger, substitution = message_body.split(command.get_trigger())
        logging.debug(f'Set substitution {trigger}')
        self._all_commands.append(SubstitutionCommand(CommandIdentifier.GET_SUBSTITUTION, trigger, substitution, security_level))
        return f'When you say: "{trigger}", I say: {substitution}'

    def _get_theme(self) -> str:
        logging.debug(f'Get theme {self._theme}')
        return self._theme

    def _set_theme(self, command: Command, message_body: str) -> str:
        self._theme = message_body[len(command.get_trigger()):]
        logging.debug(f'Set theme: {self._theme}')
        return f'Theme set to: {self._theme}'

    def _get_substitution(self, command: Command) -> str:
        logging.debug(f'Get substitution: {command}')
        return str(command)

    def _list_substitutions(self, user_identifier: str) -> str:
        logging.debug('List all substitutions')
        substitutions_string = ", ".join([command.get_trigger() for command in self._all_commands if command.has_clearance(self._get_user_security_level(user_identifier)) and command.is_substitution()])
        return f'These substitutions are set: {substitutions_string}'

    def _list_commands(self, user_identifier: str) -> str:
        logging.debug('List commands')
        commands_string = "".join([f"{command}\n" for command in self._all_commands if command.has_clearance(self._get_user_security_level(user_identifier)) and not command.is_substitution()])
        return f"These commands are available:\n{commands_string}"

    def _set_role(self, command: Command, message_body: str, role: SecurityLevel) -> str:
        user_identifier = message_body[len(command.get_trigger()):]
        if self._get_user_security_level(user_identifier) >= role:
            return "User already registered"
        self._users_registry.register_user(user_identifier, role)
        return "User registered"
