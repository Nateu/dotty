from enum import Enum, auto


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
