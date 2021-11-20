from enum import Enum, auto
from typing import List
import logging


class CommandType(Enum):
    CONTAINS = auto()
    EXACT = auto()
    SUBSTITUTION = auto()
    STARTS_WITH = auto()
    UNSET = auto()


class CommandIdentifier(Enum):
    LIST_COMMANDS = auto()
    LIST_SUBSTITUTIONS = auto()
    SET_SUBSTITUTION = auto()
    SET_THEME = auto()
    SUBSTITUTION = auto()
    GET_THEME = auto()


class Command:
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        self._trigger: str = trigger
        self._description: str = description
        self.identifier: CommandIdentifier = identifier
        self._type: CommandType = CommandType.UNSET

    def __repr__(self):
        return f'"{self._trigger}" - {self._description}'

    def has_match(self, message: str) -> bool:
        pass

    def get_trigger(self) -> str:
        return self._trigger

    def get_trigger_lower_case(self) -> str:
        return self._trigger.casefold()

    def is_substitution(self):
        return self._type == CommandType.SUBSTITUTION


class StartsWithCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        super().__init__(identifier, trigger, description)
        self._type: CommandType = CommandType.STARTS_WITH

    def has_match(self, message: str) -> bool:
        logging.debug(f"Starts with: [{self.get_trigger_lower_case()}] > [{message.casefold()}]")
        return message.casefold().startswith(self.get_trigger_lower_case())


class ContainsCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        super().__init__(identifier, trigger, description)
        self._type: CommandType = CommandType.CONTAINS

    def has_match(self, message: str) -> bool:
        logging.debug(f"Checking: [{self.get_trigger_lower_case()}] in [{message.casefold()}]")
        return self.get_trigger_lower_case() in message.casefold()


class ExactCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        super().__init__(identifier, trigger, description)
        self._type: CommandType = CommandType.EXACT

    def has_match(self, message: str) -> bool:
        logging.debug(f"Comparing: [{self.get_trigger_lower_case()}] and [{message.casefold()}] {self.get_trigger_lower_case() == message.casefold()}")
        return self.get_trigger_lower_case() == message.casefold()


class SubstitutionCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, substitution: str):
        super().__init__(identifier, trigger, "substitution")
        self._type: CommandType = CommandType.SUBSTITUTION
        self._substitution = substitution

    def has_match(self, message: str) -> bool:
        logging.debug(f"Comparing: [{self.get_trigger_lower_case()}] and [{message.casefold()}] {self.get_trigger_lower_case() == message.casefold()}")
        return self.get_trigger_lower_case() == message.casefold()

    def __repr__(self):
        return self._substitution


class Commands:
    def __init__(self, name: str = "Dotty"):
        self._name: str = name
        self._theme: str = 'No theme set'
        self._all_commands: List[Command] = []
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.LIST_COMMANDS,
                "Usage",
                "List all commands and their usage"
            )
        )
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.LIST_SUBSTITUTIONS,
                "List",
                "List all substitutions"
            )
        )
        self._all_commands.append(
            ContainsCommand(
                CommandIdentifier.SET_SUBSTITUTION,
                " -> ",
                f'On the trigger (before) -> {self._name} will respond with message (after)',
            )
        )
        self._all_commands.append(
            ExactCommand(
                CommandIdentifier.GET_THEME,
                "Theme",
                f'This will give back the current theme',
            )
        )
        self._all_commands.append(
            StartsWithCommand(
                CommandIdentifier.SET_THEME,
                "Set Theme ",
                f'This will set a theme, anything after "set theme " will be the theme',
            )
        )

    def process_message(self, message):
        for command in self._all_commands:
            logging.debug(f"Checking Command: {command.get_trigger_lower_case()}")
            if command.has_match(message):
                logging.debug(f"Found a match: {command.get_trigger_lower_case()}")
                return self._process_command(command, message)

    def _process_command(self, command, message):
        match command.identifier:
            case CommandIdentifier.LIST_COMMANDS:
                return self._list_commands()
            case CommandIdentifier.LIST_SUBSTITUTIONS:
                return self._list_substitutions()
            case CommandIdentifier.SUBSTITUTION:
                return self._apply_substitution(command)
            case CommandIdentifier.SET_THEME:
                return self._set_theme(command, message)
            case CommandIdentifier.GET_THEME:
                return self._get_theme()
            case CommandIdentifier.SET_SUBSTITUTION:
                return self._set_substitution(message)

    def _set_substitution(self, message):
        logging.debug(' -> ')
        trigger, substitution = message.split(' -> ')
        self._all_commands.append(
            SubstitutionCommand(
                CommandIdentifier.SUBSTITUTION,
                trigger,
                substitution
            )
        )
        return f'When you say: "{trigger}", I say: {substitution}'

    def _get_theme(self):
        logging.debug(f'Get theme {self._theme}')
        return self._theme

    def _set_theme(self, command, message):
        self._theme = message[len(command.get_trigger()):]
        logging.debug(f'set theme: {self._theme}')
        return f'Theme set to: {self._theme}'

    def _apply_substitution(self, command):
        logging.debug(f'substitution -> {command}')
        return str(command)

    def _list_substitutions(self):
        logging.debug('list')
        substitutions_string = ", ".join([command.get_trigger() for command in self._all_commands if command.is_substitution()])
        return f'These substitutions are set: {substitutions_string}'

    def _list_commands(self):
        logging.debug('usage')
        commands_string = "".join([f"{command}\n" for command in self._all_commands if not command.is_substitution()])
        return f"These commands are available:\n{commands_string}"
