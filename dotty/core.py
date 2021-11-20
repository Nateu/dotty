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
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        self._trigger: str = trigger
        self._description: str = description
        self.identifier: CommandIdentifier = identifier
        self._type: CommandType = CommandType.UNSET

    def __repr__(self):
        return f'"{self._trigger}" - {self._description}'

    def has_match(self, message_body: str) -> bool:
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

    def has_match(self, message_body: str) -> bool:
        logging.debug(f"Starts with: [{self.get_trigger_lower_case()}] > [{message_body.casefold()}]")
        return message_body.casefold().startswith(self.get_trigger_lower_case())


class ContainsCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        super().__init__(identifier, trigger, description)
        self._type: CommandType = CommandType.CONTAINS

    def has_match(self, message_body: str) -> bool:
        logging.debug(f"Checking: [{self.get_trigger_lower_case()}] in [{message_body.casefold()}]")
        return self.get_trigger_lower_case() in message_body.casefold()


class ExactCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, description: str):
        super().__init__(identifier, trigger, description)
        self._type: CommandType = CommandType.EXACT

    def has_match(self, message_body: str) -> bool:
        logging.debug(f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] {self.get_trigger_lower_case() == message_body.casefold()}")
        return self.get_trigger_lower_case() == message_body.casefold()


class SubstitutionCommand(Command):
    def __init__(self, identifier: CommandIdentifier, trigger: str, substitution: str):
        super().__init__(identifier, trigger, "substitution")
        self._type: CommandType = CommandType.SUBSTITUTION
        self._substitution = substitution

    def has_match(self, message_body: str) -> bool:
        logging.debug(f"Comparing: [{self.get_trigger_lower_case()}] and [{message_body.casefold()}] {self.get_trigger_lower_case() == message_body.casefold()}")
        return self.get_trigger_lower_case() == message_body.casefold()

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

    def process_message(self, message: Message) -> str:
        for command in self._all_commands:
            logging.debug(f"Checking Command: {command.get_trigger()}")
            if command.has_match(message.body):
                logging.debug(f"Found a match: {command.get_trigger_lower_case()}")
                return self._process_command(command, message)

    def _process_command(self, command: Command, message: Message) -> str:
        match command.identifier:
            case CommandIdentifier.LIST_COMMANDS:
                return self._list_commands()
            case CommandIdentifier.LIST_SUBSTITUTIONS:
                return self._list_substitutions()
            case CommandIdentifier.SUBSTITUTION:
                return self._apply_substitution(command)
            case CommandIdentifier.SET_THEME:
                return self._set_theme(command, message.body)
            case CommandIdentifier.GET_THEME:
                return self._get_theme()
            case CommandIdentifier.SET_SUBSTITUTION:
                return self._set_substitution(command, message.body)

    def _set_substitution(self, command: Command, message_body: str) -> str:
        trigger, substitution = message_body.split(command.get_trigger())
        logging.debug(f'Set substitution {trigger}')
        self._all_commands.append(SubstitutionCommand(CommandIdentifier.SUBSTITUTION, trigger, substitution))
        return f'When you say: "{trigger}", I say: {substitution}'

    def _get_theme(self) -> str:
        logging.debug(f'Get theme {self._theme}')
        return self._theme

    def _set_theme(self, command: Command, message_body: str) -> str:
        self._theme = message_body[len(command.get_trigger()):]
        logging.debug(f'Set theme: {self._theme}')
        return f'Theme set to: {self._theme}'

    def _apply_substitution(self, command: Command) -> str:
        logging.debug(f'Apply substitution: {command}')
        return str(command)

    def _list_substitutions(self) -> str:
        logging.debug('List all substitutions')
        substitutions_string = ", ".join([command.get_trigger() for command in self._all_commands if command.is_substitution()])
        return f'These substitutions are set: {substitutions_string}'

    def _list_commands(self) -> str:
        logging.debug('List commands')
        commands_string = "".join([f"{command}\n" for command in self._all_commands if not command.is_substitution()])
        return f"These commands are available:\n{commands_string}"
