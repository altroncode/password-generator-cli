import argparse
import contextlib
import json
import urllib.error
import urllib.parse
import urllib.request

import color
import config
import password

parser = argparse.ArgumentParser(prog='password_generator', description='Generate password and send it to telegram')
parser.add_argument('--length', '-l', type=int, dest='length', default=32, nargs='?')
parser.add_argument('--platform', '-p', type=str, dest='platform', default='-', nargs='?')
parser.add_argument('--email', '-e', type=str, dest='email',
                    default=config.data.PasswordGeneratorData.email)
parser.add_argument('--username', '-u', type=str, dest='username', default='-', nargs='?')
parser.add_argument('--send', type=str, dest='send', default='telegram', nargs='?')
parser.add_argument('--password', '-ps', type=str, dest='password', nargs='?')
parser.add_argument('--note', '-n', action='store_true', dest='note')
parser.add_argument('--symbols', '-s', type=str, dest='symbols', default='dlp', nargs='?')
arguments = parser.parse_args()

password = arguments.password or password.Password(
    length=arguments.length,
    is_digit='d' in arguments.symbols,
    is_letter='l' in arguments.symbols,
    is_punctuation='p' in arguments.symbols
)

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
        "chat_id": chat_id
    }
    return urllib.parse.urlencode(data | kwargs).encode("utf-8")


if arguments.telegram == 'telegram':

    url = f'https://api.telegram.org/bot{config.data.TelegramData.token}'
    send_message_url = f'{url}/sendMessage'
    delete_message_url = f'{url}/deleteMessage'

    try:
        with contextlib.suppress(urllib.error.URLError):
            urllib.request.urlopen(delete_message_url, prepare_data(
                config.data.TelegramData.user_id,
                message_id=config.data.TelegramData.last_message_id))
        urllib.request.urlopen(send_message_url, prepare_data(config.data.TelegramData.user_id, generate_message()))
        urllib.request.urlopen(send_message_url, prepare_data(config.data.TelegramData.user_id,
                                                              f'`{escape_message(password)}`'))
        response = urllib.request.urlopen(send_message_url, prepare_data(config.data.TelegramData.user_id,
                                                                         f'`{"*" * 42}`'))

        config.data.config.set('config', 'last_message_id', str(json.loads(response.read())['result']['message_id']))

        with open(config.data.config_path, 'w') as config_file:
            config.data.config.write(config_file)

    except urllib.error.HTTPError:
        print(color.color_text(color.Colors.ERROR, 'Something went wrong!!!'))
    else:
        print(color.color_text(color.Colors.SUCCESS, 'Success!'))
