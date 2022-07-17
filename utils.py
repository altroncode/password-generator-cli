def escape_message(message: str) -> str:
    return "".join([f'\\{i}' for i in message])
