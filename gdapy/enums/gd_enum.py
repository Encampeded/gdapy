from enum import Enum

from pyheck import title


class GDEnum(Enum):
    def __repr__(self):
        return title(self.name)
