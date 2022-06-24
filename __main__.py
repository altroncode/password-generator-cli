import urllib.request
import urllib.parse
import urllib.error
import contextlib
import json
import sys

import password
import config
import color
import cli


arguments = cli.get_arguments(argument_parser=cli.parser, args=sys.argv)

password_settings = config.settings.PasswordSettings()
password_settings.digits_in_password = arguments.digits_in_password
password_settings.capital_letters_in_password = arguments.capital_letters_in_password
password_settings.small_letters_in_password = arguments.small_letters_in_password
password_settings.punctuation_in_password = arguments.punctuation_in_password

password = arguments.password or password.Password(settings=password_settings)

print(password)


def escape_message(message: str) -> str:
    return "".join([f'\\{i}' for i in message])


def create_message() -> str:
    message = f'*Platform*: {escape_message(arguments.platform)}\n' \
              f'*Email*: {escape_message(arguments.email)}\n' \
              f'*Username*: {escape_message(arguments.username)}\n'

    if arguments.note:
        note = create_note()
        return f'{message}*Note*: {note}' if note else message

    return message


def create_note() -> str:
    note = []
    print()
    line = input("Note: ")
    while line:
        note.append(line)
        line = input()
    return '\n'.join(note)


def prepare_data(chat_id: int, text: str = "", **kwargs) -> bytes:
    data = {
        "text": text,
        "parse_mode": "MarkdownV2",
        "chat_id": chat_id
    }
    return urllib.parse.urlencode(data | kwargs).encode("utf-8")


if arguments.send == 'telegram':

    telegram_data = config.data.TelegramData()
    url = f'https://api.telegram.org/bot{telegram_data.token}'
    send_message_url = f'{url}/sendMessage'
    delete_message_url = f'{url}/deleteMessage'

    try:
        with contextlib.suppress(urllib.error.URLError):
            urllib.request.urlopen(delete_message_url, prepare_data(
                telegram_data.user_id,
                message_id=telegram_data.last_message_id))
        urllib.request.urlopen(send_message_url, prepare_data(telegram_data.user_id, create_message()))
        urllib.request.urlopen(send_message_url, prepare_data(telegram_data.user_id,
                                                              f'`{escape_message(password)}`'))
        response = urllib.request.urlopen(send_message_url, prepare_data(telegram_data.user_id,
                                                                         f'`{"*" * 42}`'))

        telegram_data.last_message_id = str(json.loads(response.read())['result']['message_id'])
        telegram_data.save()

    except urllib.error.HTTPError:
        print(color.color_text(color.Colors.ERROR, 'Something went wrong!!!'))
    else:
        print(color.color_text(color.Colors.SUCCESS, 'Success!'))
