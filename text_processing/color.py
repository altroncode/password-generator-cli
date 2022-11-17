import enum
import random


class StatusColor(str, enum.Enum):
    ERROR: str = random.choice(('\033[31m', '\033[91m'))
    SUCCESS: str = random.choice(('\033[32m', '\033[92m'))
    INFO: str = random.choice(('\033[34m', '\033[94m'))
    WARNING: str = random.choice(('\033[33m', '\033[93m'))

    def __str__(self):
        return self.value
