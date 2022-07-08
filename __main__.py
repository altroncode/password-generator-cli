import urllib.error
import sys

from data.data_sources import data_sources
from data import settings
from data import app_data
import password_info
import strorages
import password
import color
import cli


arguments = cli.get_arguments(argument_parser=cli.parser, args=sys.argv[1:])

data_source = data_sources.CLIArgumentsDataSource(arguments) + data_sources.IniDataSource(settings.SETTINGS_PATH)
password_settings = settings.PasswordSettings(source=data_source)
general_settings = settings.GeneralSettings(source=data_source)
password = arguments.password or password.Password(settings=password_settings)

print(password)


def create_note() -> str:
    note = []
    print()
    line = input("Note: ")
    while line:
        note.append(line)
        line = input()
    return '\n'.join(note)


storages_dict = {'telegram': strorages.TelegramStorage}
password_info_builders = {'telegram': password_info.TelegramPasswordInfoBuilder}
storage_datas = {'telegram': app_data.TelegramData}

for storage_name in general_settings.storages:
    storage_data = storage_datas.get(storage_name)
    storage = storages_dict.get(storage_name)(storage_data(source=data_source))
    builder = password_info_builders.get(storage_name)

    password_info_data = app_data.PasswordInfoData(source=data_source)
    telegram_password_director = password_info.PasswordInfoDirector(data=password_info_data)
    password_info_message = telegram_password_director.create_password_info(
        builder=builder()
    )
    try:
        storage.keep(password, password_info_message)
    except urllib.error.HTTPError:
        color.print_colored_text(color.Colors.ERROR, 'Something went wrong!!!')
    else:
        color.print_colored_text(color.Colors.SUCCESS, 'Success!')
