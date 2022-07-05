import random


class Colors:
    @property
    def error(self):
        return random.choice(('\033[31m', '\033[91m'))

    @property
    def success(self):
        return random.choice(('\033[32m', '\033[92m'))

    @property
    def warning(self):
        return random.choice(('\033[33m', '\033[93m'))

    @property
    def info(self):
        return random.choice(('\033[34m', '\033[94m'))
