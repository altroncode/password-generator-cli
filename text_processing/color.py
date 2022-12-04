import enum
import random


__all__ = ('Color', 'StatusColor')


class Color(str, enum.Enum):
    RED: str = random.choice(('\033[31m', '\033[91m'))
    GREEN: str = random.choice(('\033[32m', '\033[92m'))
    BLUE: str = random.choice(('\033[34m', '\033[94m'))
    YELLOW: str = random.choice(('\033[33m', '\033[93m'))

    def __str__(self):
        return self.value


class StatusColor(str, enum.Enum):
    ERROR: str = Color.RED
    SUCCESS: str = Color.GREEN
    INFO: str = Color.BLUE
    WARNING: str = Color.YELLOW

    def __str__(self):
        return self.value
