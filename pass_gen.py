from configparser import ConfigParser
from contextlib import suppress
from random import choice
from pathlib import Path
import urllib.request
import urllib.parse
import urllib.error
import argparse
import string
import json


config = ConfigParser()
filename = Path.home() / '.local/share/password_generator/config.ini'
config.read(filename)

parser = argparse.ArgumentParser(prog='password_generator', description='Generate password and send it')
parser.add_argument('--length', '-l', type=int, dest='length', default=32, nargs='?')
parser.add_argument('--platform', '-p', type=str, dest='platform', default='-', nargs='?')
parser.add_argument('--email', '-e', type=str, dest='email',
                    default=config.get('config', 'email'), nargs='?')
parser.add_argument('--username', '-u', type=str, dest='username', default='-', nargs='?')
parser.add_argument('--telegram', '-tg', type=str, dest='telegram', nargs='?')
parser.add_argument('--password', '-ps', type=str, dest='password', nargs='?')
parser.add_argument('--note', '-n', action='store_true', dest='note')
parser.add_argument('--symbols', '-s', type=str, dest='symbols', default='dlp', nargs='?')
arguments = parser.parse_args()


def generate_password(length: int) -> str:
    symbols = (
        f'{string.digits if "d" in arguments.symbols else ""}'
        f'{string.ascii_letters if "l" in arguments.symbols else ""}'
        f'{string.punctuation if "p" in arguments.symbols else ""}'
    )

    return str().join(choice(symbols) for _ in range(length))


password = arguments.password or generate_password(length=arguments.length)
print(password)


def escape_message(message: str) -> str:
    return str().join([f'\\{i}' for i in message])


def generate_message() -> str:
    message = f'*Platform*: {escape_message(arguments.platform)}\n' \
              f'*Email*: {escape_message(arguments.email)}\n' \
              f'*Username*: {escape_message(arguments.username)}\n'

    if arguments.note:
        note = generate_note()
        return f'{message}*Note*: {note}' if note else message

    return message


def generate_note() -> str:
    note = []
    print()
    line = input("Note: ")
    while line:
        note.append(line)
        line = input()
    return '\n'.join(note)


def prepare_data(chat_id: int, text: str = str(), **kwargs) -> bytes:
    data = {
        "text": text,
        "parse_mode": "MarkdownV2",
        "chat_id": chat_id,
    }
    return urllib.parse.urlencode(data | kwargs).encode("utf-8")


if arguments.telegram != 'False':

    user_id = int(config.get('config', 'user_id'))
    tg_bot_token = config.get('config', 'tg_bot_token')
    message_id = int(config.get('config', 'last_message_id'))

    url = f'https://api.telegram.org/bot{tg_bot_token}'
    send_message_url = f'{url}/sendMessage'
    delete_message_url = f'{url}/deleteMessage'

    try:
        with suppress(urllib.error.URLError):
            urllib.request.urlopen(delete_message_url, prepare_data(user_id, message_id=message_id))
        urllib.request.urlopen(send_message_url, prepare_data(user_id, generate_message()))
        urllib.request.urlopen(send_message_url, prepare_data(user_id, f'`{escape_message(password)}`'))
        response = urllib.request.urlopen(send_message_url, prepare_data(user_id, f'`{"*" * 42}`'))

        config.set('config', 'last_message_id', str(json.loads(response.read())['result']['message_id']))

        with open(filename, 'w') as configfile:
            config.write(configfile)

    except urllib.error.HTTPError:
        print('\033[91m' + 'Something went wrong!!!')
