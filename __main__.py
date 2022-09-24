import sys

from config.data_sources import data_sources
from config import settings
from config import app_data
import password_info
import strorages
import exception
import password
import color
import cli


arguments = cli.get_arguments(argument_parser=cli.parser, args=sys.argv[1:])

settings_source = data_sources.CLIArgumentsDataSource(arguments) + data_sources.IniDataSource(settings.SETTINGS_PATH)
password_settings = settings.PasswordSettings(source=settings_source)
general_settings = settings.GeneralSettings(source=settings_source)
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
password_info_builders = {'telegram': password_info.TelegramPasswordInfoBuilder}
storage_datas = {'telegram': app_data.TelegramData}

for storage_name in general_settings.storages:
    data_source = data_sources.CLIArgumentsDataSource(arguments) + data_sources.IniDataSource(settings.DATA_PATH)
    storage_data = storage_datas.get(storage_name)
    storage = storages_dict.get(storage_name)(storage_data(source=data_source))
    builder = password_info_builders.get(storage_name)

    password_info_data = app_data.PasswordInfoData(source=data_source)
    if password_info_data.is_note:
        password_info_data.note = create_note()
    telegram_password_director = password_info.PasswordInfoDirector(data=password_info_data)
    password_info_message = telegram_password_director.create_password_info(
        builder=builder()
    )
    try:
        storage.keep(password, password_info_message)
    except exception.KeepPasswordError:
        color.print_colored_text(color.Colors.ERROR, 'Something went wrong!!!')
    else:
        color.print_colored_text(color.Colors.SUCCESS, 'Success!')
