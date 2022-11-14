import sys

import cli
import color
import exception
import password
import credentials
import strorages
from config import settings
from config.data_sources import data_sources

arguments = cli.get_arguments(argument_parser=cli.parser, args=sys.argv[1:])

data_source = (data_sources.CLIArgumentsDataSource(arguments) +
               data_sources.IniDataSource(settings.SETTINGS_PATH) +
               data_sources.EnvDataSource(settings.ENV_PATH))
password_settings = settings.PasswordSettings(source=data_source)
general_settings = settings.GeneralSettings(source=data_source)
password = arguments.password or str(password.Password(settings=password_settings))

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
password_info_builders = {'telegram': credentials.TelegramPasswordInfoBuilder}
storage_settings_dict = {'telegram': settings.TelegramSettings}

for storage_name in general_settings.storages:
    storage_settings = storage_settings_dict.get(storage_name)
    storage = storages_dict.get(storage_name)(storage_settings(source=data_source))
    builder = password_info_builders.get(storage_name)

    password_info_settings = settings.PasswordInfoSettings(source=data_source)
    if password_info_settings.is_note:
        password_info_settings.note = create_note()
    telegram_password_director = credentials.PasswordInfoDirector(password_info_settings)
    password_info_message = telegram_password_director.create_password_info(builder=builder())
    try:
        storage.keep(password, password_info_message)
    except exception.KeepPasswordError:
        color.print_colored_text(color.Colors.ERROR, 'Something went wrong!!!')
    else:
        color.print_colored_text(color.Colors.SUCCESS, 'Success!')
