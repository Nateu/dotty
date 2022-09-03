from enum import Enum
from functools import total_ordering

import json_fix  # noqa:F401


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

    def __json__(self):
        return self.value
