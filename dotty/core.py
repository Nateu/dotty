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
    SUBSTITUTION = auto()


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
        self._name = name
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

    def _get_commands(self) -> str:
        return "".join([f"{command}\n" for command in self._all_commands if not command.is_substitution()])

    def print_commands(self) -> str:
        return f"These commands are available:\n{self._get_commands()}"

    def _get_substitutions(self) -> str:
        subs = [command.get_trigger() for command in self._all_commands if command.is_substitution()]
        logging.debug(f"Subs: {', '.join(subs)}")
        return ", ".join(subs)

    def process_message(self, message):
        logging.debug(f"Hello, my name is {self._name}.")
        response = ''
        for command in self._all_commands:
            logging.debug(f"Checking Command: {command.get_trigger_lower_case()}")
            if command.has_match(message):
                logging.debug(f"Found a match: {command.get_trigger_lower_case()}")
                match command.identifier:
                    case CommandIdentifier.LIST_COMMANDS:
                        logging.debug('usage')
                        response = self.print_commands()
                        break
                    case CommandIdentifier.LIST_SUBSTITUTIONS:
                        logging.debug('list')
                        response = F'These substitutions are set: {self._get_substitutions()}'
                        break
                    case CommandIdentifier.SET_SUBSTITUTION:
                        logging.debug(' -> ')
                        trigger, substitution = message.split(' -> ')
                        self._all_commands.append(
                            SubstitutionCommand(
                                CommandIdentifier.SUBSTITUTION,
                                trigger,
                                substitution
                            )
                        )
                        response = F'When you say: "{trigger}", I say: {substitution}'
                        break
                    case CommandIdentifier.SUBSTITUTION:
                        logging.debug(f'substitution -> {command}')
                        response = str(command)
                        break
        return response
