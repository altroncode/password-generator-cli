import urllib.request
import urllib.parse
import urllib.error
import contextlib
import json
import sys

from data.data_sources import data_sources
from data import settings
from data import app_data
import password_info
import password
import color
import cli


arguments = cli.get_arguments(argument_parser=cli.parser, args=sys.argv[1:])

data_source = data_sources.CLIArgumentsDataSource(arguments) + data_sources.IniDataSource(settings.SETTINGS_PATH)
password_settings = settings.PasswordSettings(source=data_source)
password = arguments.password or password.Password(settings=password_settings)

print(password)


def escape_message(message: str) -> str:
    return "".join([f'\\{i}' for i in message])


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

    telegram_data = app_data.TelegramData(source=data_sources.IniDataSource(settings.DATA_PATH))
    url = f'https://api.telegram.org/bot{telegram_data.token}'
    send_message_url = f'{url}/sendMessage'
    delete_message_url = f'{url}/deleteMessage'
    password_info_data = app_data.PasswordInfoData(source=data_source)
    telegram_password_director = password_info.PasswordInfoDirector(data=password_info_data)
    password_info_message = telegram_password_director.create_password_info(
        builder=password_info.TelegramPasswordInfoBuilder()
    )
    try:
        with contextlib.suppress(urllib.error.URLError):
            urllib.request.urlopen(delete_message_url, prepare_data(
                telegram_data.user_id,
                message_id=telegram_data.last_message_id))
        urllib.request.urlopen(send_message_url, prepare_data(telegram_data.user_id, password_info_message))
        urllib.request.urlopen(send_message_url, prepare_data(telegram_data.user_id,
                                                              f'`{escape_message(password)}`'))
        response = urllib.request.urlopen(send_message_url, prepare_data(telegram_data.user_id,
                                                                         f'`{"*" * 42}`'))

        telegram_data.last_message_id = str(json.loads(response.read())['result']['message_id'])
        telegram_data['last_message_id'].save()

    except urllib.error.HTTPError:
        color.print_colored_text(color.Colors.ERROR, 'Something went wrong!!!')
    else:
        color.print_colored_text(color.Colors.SUCCESS, 'Success!')
