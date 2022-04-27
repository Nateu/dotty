from enum import Enum, auto


class CommandIdentifier(Enum):
    LIST_COMMANDS = auto()
    SET_THEME = auto()
    GET_THEME = auto()
    SET_USER_SUBSTITUTION = auto()
    SET_ADMIN_SUBSTITUTION = auto()
    LIST_SUBSTITUTIONS = auto()
    GET_SUBSTITUTION = auto()
    SET_ROLE_OWNER = auto()
    REMOVE_ROLE_OWNER = auto()
    SET_ROLE_ADMIN = auto()
    REMOVE_ROLE_ADMIN = auto()
    SET_ROLE_USER = auto()
    REMOVE_ROLE_USER = auto()
    UNSET = auto()
