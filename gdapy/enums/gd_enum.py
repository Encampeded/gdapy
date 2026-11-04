from enum import Enum

from pyheck import title


class GDEnum(Enum):
    def __str__(self):
        return title(self.name)
