import typing


def print_colored_text(color: str, text: typing.Any) -> None:
    print(f'{color}{text}\x1b[0m')
