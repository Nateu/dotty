from typing import List, Optional

from bot.command import Command, ContainsCommand, ExactCommand, StartsWithCommand, SubstitutionCommand
from bot.command_identifier import CommandIdentifier
from bot.security_level import SecurityLevel


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
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.LIST_USERS,
                "User List",
                "List all known Users",
                SecurityLevel.ADMIN,
            )
        )

    def get_matching_command(self, message: str, user_security_level: SecurityLevel) -> Optional[Command]:
        for command in self._all_commands:
            if command.has_match(message, user_security_level):
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
