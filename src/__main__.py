#!/usr/bin/env python3

import sys

import cli
import note
import password
import password_saving_strategy
from config import settings
from config.data_sources import data_sources


def main():
    parser = cli.create_parser()
    cli.configure_parser(parser)

    arguments = cli.get_arguments(argument_parser=parser, args=sys.argv[1:])

    data_source = (
            data_sources.CLIArgumentsDataSource(arguments) +
            data_sources.IniDataSource(settings.SETTINGS_PATH) +
            data_sources.EnvDataSource(settings.ENV_PATH)
    )

    app_settings = settings.AppSettings(data_source)
    password_settings = settings.PasswordSettings(data_source)
    credentials_settings = settings.CredentialsSettings(data_source)

    if arguments.password:
        password_ = password.Password(arguments.password)
    else:
        password_ = password.PasswordFactory(settings=password_settings).create_password()

    print(password_)

    password_saving_strategies = {
        'telegram': password_saving_strategy.PasswordSavingToTelegramStrategy()
    }

    for password_saving_method in app_settings.storages:
        strategy = password_saving_strategies.get(password_saving_method)
        note_ = note.CLINoteFactory().create_note() if credentials_settings.is_note else None
        strategy.save_password(data_source, credentials_settings, password_, note_)


if __name__ == '__main__':
    main()
