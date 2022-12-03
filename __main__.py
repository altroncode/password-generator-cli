import sys
import typing

import cli
import note
import password
from config import settings
from config.data_sources import data_sources
import password_saving_strategy


def main():
    arguments = cli.get_arguments(argument_parser=cli.parser, args=sys.argv[1:])

    data_source = (
            data_sources.CLIArgumentsDataSource(arguments) +
            data_sources.IniDataSource(settings.SETTINGS_PATH) +
            data_sources.EnvDataSource(settings.ENV_PATH)
    )

    password_settings = settings.PasswordSettings(data_source)
    app_settings = settings.AppSettings(data_source)
    credentials_settings = settings.CredentialsSettings(data_source)

    password_ = (password.Password(arguments.password) or
                 password.PasswordFactory(settings=password_settings))
    print(password_)

    password_saving_strategies: dict[str, typing.Type[password_saving_strategy.BasePasswordSavingStrategy]] = {
        'telegram': password_saving_strategy.PasswordSavingToTelegramStrategy
    }

    for password_saving_method in app_settings.storages:
        strategy: password_saving_strategy.BasePasswordSavingStrategy = \
            password_saving_strategies.get(password_saving_method)()
        note_ = note.CLINoteFactory().create_note() if credentials_settings.is_note else None
        strategy.save_password(data_source, credentials_settings, password_, note_)


if __name__ == '__main__':
    main()
