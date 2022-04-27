import logging
from typing import List, Optional

from dotty.command_identifier import CommandIdentifier
from dotty.command_type import CommandType
from dotty.message import Message
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
            f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] "
            f"{self.get_trigger_lower_case() == message_body.casefold()}"
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
            f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] "
            f"{self.get_trigger_lower_case() == message_body.casefold()} "
        )
        return self.get_trigger_lower_case() == message_body.casefold()

    def __repr__(self):
        return self._substitution


class CommandRegistry:
    def __init__(self, bot_name: str = "Dotty"):
        self._bot_name = bot_name
        self._all_commands: List[Command] = []
        self._all_commands.append(
            ExactCommand(CommandIdentifier.LIST_COMMANDS, "Usage", "List all commands and their usage", SecurityLevel.USER)
        )
        self._all_commands.append(ExactCommand(CommandIdentifier.LIST_SUBSTITUTIONS, "List", "List all substitutions", SecurityLevel.USER))
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_USER_SUBSTITUTION,
                " -> ",
                f"On the trigger (before) -> {self._bot_name} will respond with message (after) [USERS]",
                SecurityLevel.ADMIN,
            )
        )
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_ADMIN_SUBSTITUTION,
                " => ",
                f"On the trigger (before) => {self._bot_name} will respond with message (after) [ADMINS]",
                SecurityLevel.ADMIN,
            )
        )
        self._all_commands.append(
            ExactCommand(CommandIdentifier.GET_THEME, "Theme", "This will give back the current theme", SecurityLevel.USER)
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

    def get_matching_command(self, message: Message, user_security_level: SecurityLevel):
        logging.debug(f"User: {message.sent_by}, {user_security_level}")
        for command in self._all_commands:
            logging.debug(f"Checking Command: {command.get_trigger()}")
            if command.has_match(message.body, user_security_level):
                return command

    def get_commands_string(self, user_security_level: SecurityLevel) -> str:
        return "".join(
            [
                f"{command}\n"
                for command in self._all_commands
                if command.has_clearance(user_security_level) and not command.is_substitution()
            ]
        )

    def get_substitution_listing(self, user_security_level: SecurityLevel):
        return ", ".join(
            [
                command.get_trigger()
                for command in self._all_commands
                if command.has_clearance(user_security_level) and command.is_substitution()
            ]
        )

    def register_substitution(self, trigger: str, substitution: str, security_level: SecurityLevel) -> Optional[Command]:
        if trigger in [command.get_trigger() for command in self._all_commands]:
            if security_level < [command.get_security_level() for command in self._all_commands if command.get_trigger() == trigger].pop():
                return
        self._all_commands = [command for command in self._all_commands if command.get_trigger() != trigger]
        new_command = SubstitutionCommand(
            identifier=CommandIdentifier.GET_SUBSTITUTION,
            trigger=trigger,
            substitution=substitution,
            security_level=security_level,
        )
        self._all_commands.append(new_command)
        return new_command
