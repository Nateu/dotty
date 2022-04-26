import logging
from typing import List, Optional

from dotty.command import Command, ContainsCommand, ExactCommand, StartsWithCommand, SubstitutionCommand
from dotty.command_identifier import CommandIdentifier
from dotty.message import Message
from dotty.security_level import SecurityLevel
from dotty.user import UserRegistry


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
                return self._set_substitution(
                    command=command, message_body=message.body, security_level=SecurityLevel.USER
                )
            case CommandIdentifier.SET_ADMIN_SUBSTITUTION:
                return self._set_substitution(
                    command=command, message_body=message.body, security_level=SecurityLevel.ADMIN
                )
            case CommandIdentifier.SET_ROLE_USER:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.USER)
            case CommandIdentifier.SET_ROLE_ADMIN:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.ADMIN)
            case CommandIdentifier.SET_ROLE_OWNER:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.OWNER)
            case CommandIdentifier.REMOVE_ROLE_OWNER:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.ADMIN, revoke=True)
            case CommandIdentifier.REMOVE_ROLE_ADMIN:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.USER, revoke=True)
            case CommandIdentifier.REMOVE_ROLE_USER:
                return self._set_role(command=command, message_body=message.body, role=SecurityLevel.GUEST, revoke=True)

    def _set_substitution(self, command: Command, message_body: str, security_level: SecurityLevel) -> Optional[str]:
        trigger, substitution = message_body.split(command.get_trigger())
        logging.debug(f"Set substitution {trigger}")
        if trigger in [command.get_trigger() for command in self._all_commands]:
            if (
                security_level
                < [
                    command.get_security_level() for command in self._all_commands if command.get_trigger() == trigger
                ].pop()
            ):
                return
        self._all_commands = [command for command in self._all_commands if command.get_trigger() != trigger]
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
