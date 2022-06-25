import enum
import random


class Colors(enum.Enum, str):
    ERROR = '\033[31m', '\033[91m'
    SUCCESS = '\033[32m', '\033[92m'
    WARNING = '\033[33m', '\033[93m'
    INFO = '\033[34m', '\033[94m'

    def __str__(self):
        return random.choice(self.value)


def color_text(color: str, text: str):
    return f'{color}{text}\x1b[0m'
